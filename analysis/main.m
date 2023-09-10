jsonStr = fileread('leokeystrokes.txt');
jsonData = jsondecode(jsonStr);

NVARS = 9;
NTRIALS = 10;

%aux = zeros(NVARS, NTRIALS);
variableNames = {'avgPress', 'avgJump', 'stdPress', 'stdJump', 'nBack', ...
                'longPress', 'shortPress', 'longJump', 'shortJump'};
userProfile = table('Size', [NTRIALS, NVARS], 'VariableTypes', ...
    repmat({'double'}, 1, NVARS), 'VariableNames', variableNames);

% check if jsonObj is an array (of right size)
if isstruct(jsonData) && numel(jsonData) == (NVARS+1)*(NTRIALS+1)
    % iterate through each list
    for rowIdx = 1:NTRIALS
        currList = jsonData(rowIdx, :);
        % check if current list is a cell array (containing dict)
        if isstruct(currList)
            result = params_for_trial(currList);

            % check if result is valid size
            if isequal(size(result), [1, NVARS])
                userProfile(rowIdx, :) = num2cell(result);
            end
        end
    end
end

avgs = mean(userProfile, 1);
stds = std(userProfile, 0);