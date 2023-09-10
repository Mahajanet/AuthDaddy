function lambdas = params_for_trial(biometrics)
    numEntries = numel(biometrics);
    timeReleased = zeros(1, numEntries);
    timePressed = zeros(1, numEntries);
    %keys = zeros(1, numEntries);
    backcount = 0;

    for idx = 1:numel(biometrics)
        if (isempty(biometrics(1, idx).timereleased))
            timeReleased(1, idx) = biometrics(1, idx).timepressed + 100;
        else
            timeReleased(1, idx) = biometrics(1, idx).timereleased;
        end
        timePressed(1, idx) = biometrics(1, idx).timepressed;
        if biometrics(1, idx).key == "Backspace"
            backcount.increment();
        end
    end

    keyPress = timeReleased - timePressed;
    keyJump = diff(timePressed);

    lambdas = [];

    % avg time per key press
    lambdas = [lambdas, mean(keyPress)];
    
    % avg time between key presses
    lambdas = [lambdas, mean(keyJump)];
    
    % std time per key press
    lambdas = [lambdas, std(keyPress)];
    
    % std time between key presses
    lambdas = [lambdas, std(keyJump)];
    
    % number of back spaces
    lambdas = [lambdas, backcount];
    
    % longest key press (intra)
    lambdas = [lambdas, max(keyPress)];
    
    % shortest key press
    lambdas = [lambdas, min(keyPress)];
    
    % biggest jump (inter)
    lambdas = [lambdas, max(keyJump)];
    
    % shortest jump
    lambdas = [lambdas, min(keyJump)];

end