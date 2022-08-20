replab_init;
outcomes = [1 1 1 1;
            1 1 1 0;
            1 1 0 1;
            1 1 0 0;
            1 0 1 1;
            1 0 1 0;
            1 0 0 1;
            1 0 0 0;
            0 1 1 1;
            0 1 1 0;
            0 1 0 1;
            0 1 0 0;
            0 0 1 1;
            0 0 1 0;
            0 0 0 1;
            0 0 0 0]; 

% Define all the possible patterns
C = cell(1, 16);
[C{:}] = ndgrid([1, 0]);
C = cellfun(@(a) a(:), C, 'Uni', 0);
pattern = [C{:}];
pattern = pattern';
% Construct the group
% Represent the generators
gPerm = [];
gFlip = [];
gNot = [];
for k = 1:length(outcomes)
    gPerm = [gPerm, Gperm(outcomes(k,:), outcomes)]; % P(abcd) -> P(bcda)
    gFlip = [gFlip, Gflip(outcomes(k,:), outcomes)]; % P(abcd) -> P(cbad)
    gNot = [gNot, Gnot(outcomes(k,:), outcomes)]; % P(abcd) -> P(~abcd)
end
generators = {gPerm, gFlip, gNot};
% Define the group
S16 = replab.S(16);
H = S16.subgroup(generators);
g = H.elements;
% Construct the orbits
orbit = {};
done = [];
rep = S16.naturalRep;
for i = 1:length(pattern)
    out = ['Pattern ', int2str(length(done)), '/', int2str(length(pattern))];
    disp(out);
    arg = pattern(:,i);
    img = [];
    count = 0;
    % Check if arg is done
    if ~isempty(done)
        for j = 1:length(done(1,:))
            if arg == done(:,j)
                count = count+1;
            end
        end
    end
    if count > 0
        continue;
    else
        for k = 1:length(g)
            done = [done, rep.image(g{k}) * arg];
            img = [img, rep.image(g{k}) * arg];
        end
        inter = unique(done', 'rows');
        done = inter';
        inter = unique(img', 'rows');
        img = inter';
        orbit{end+1} = img;
    end
    
    if length(done) == length(pattern)-1
        orbit{end+1} = pattern(:, end);
        break;
    end
end
orbit(end) = [];

O_ = [];
for i = 1:length(orbit)
    O_ = [O_; orbit{i}(:,1)'];
end
writematrix(O_, 'orbit.csv');

% Represents the generators
function c = Gperm(P, outcomes)
    newP(1) = P(2);
    newP(2) = P(3);
    newP(3) = P(4);
    newP(4) = P(1);
    
    for i = 1:length(outcomes)
        if newP == outcomes(i,:)
            c = i;
        end
    end
end
    
function c = Gflip(P, outcomes)
    newP(1) = P(3);
    newP(2) = P(2);
    newP(3) = P(1);
    newP(4) = P(4);
    
    for i = 1:length(outcomes)
        if newP == outcomes(i,:)
            c = i;
        end
    end
end

function c = Gnot(P, outcomes)
    if P(1) == 1
        newP(1) = 0;
    else
        newP(1) = 1;
    end
    newP(2) = P(2);
    newP(3) = P(3);
    newP(4) = P(4);
    
    for i = 1:length(outcomes)
        if newP == outcomes(i,:)
            c = i;
        end
    end
end

    