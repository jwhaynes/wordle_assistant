function generateGuesses () {
    // main function for generating guess words

    const correctLetterValues = getCorrectLetterValues();
    const misplacedLetterValues = getMisplacedLetterValues();
    const wrongLetterValues = getWrongLetterValues();
    const misplacedLetterIncorrectLetterPositionsValues = getMisplacedLetterIncorrectLetterPositions();
    const incorrectLettersRemoved = removeIncorrectLetters(wrongLetterValues);
    const letterPossibilitiesForWord = regexPositionPossibilites(incorrectLettersRemoved, correctLetterValues);
    const refinedLetterPossibilitiesForWord = removeMisplacedLetters(letterPossibilitiesForWord, misplacedLetterValues, misplacedLetterIncorrectLetterPositionsValues);
    const regexExpression = createFinalRegexExpression(refinedLetterPossibilitiesForWord,misplacedLetterValues);



    const guessesBox = document.getElementById('guesses-box');
    guessesBox.innerHTML = regexExpression;
    console.log(regexExpression)
}

function getCorrectLetterValues () {
    // function for retreiving "correct" letters as an object with keys as letter position indices
    const correctLetters = {
        1: document.getElementById('correct-letter-1').value.toLowerCase(),
        2: document.getElementById('correct-letter-2').value.toLowerCase(),
        3: document.getElementById('correct-letter-3').value.toLowerCase(),
        4: document.getElementById('correct-letter-4').value.toLowerCase(),
        5: document.getElementById('correct-letter-5').value.toLowerCase()
    };
    return correctLetters;
}

function getMisplacedLetterValues () {
    // function for retrieving "misplaced" letters as an object with keys to correspond to checkbox columns
    const misplacedLetters = {
        1: document.getElementById('misplaced-letter-1').value.toLowerCase(),
        2: document.getElementById('misplaced-letter-2').value.toLowerCase(),
        3: document.getElementById('misplaced-letter-3').value.toLowerCase(),
        4: document.getElementById('misplaced-letter-4').value.toLowerCase(),
        5: document.getElementById('misplaced-letter-5').value.toLowerCase()
    };
    return misplacedLetters;
}

function getMisplacedLetterIncorrectLetterPositions () {
    // function to determine word indices that misplaced letter does not belong in

    // create HTML collection of all checkboxes
    const checkBoxes = document.getElementsByClassName('misplaced-letter-checkbox');

    // create object to hold a list of indices for each misplaced letter
    const misplacedLetterIncorrectLetterPositions = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: []
    };

    // loop through each checkbox; if checkbox is checked... push it's position to appropriate list in object
    for (let checkBox of checkBoxes) {
        if (checkBox.checked === true) {
            misplacedLetterIncorrectLetterPositions[checkBox.id[17]].push(checkBox.id[checkBox.id.length-1]);
        }
    };
    
    return misplacedLetterIncorrectLetterPositions;
}

function getWrongLetterValues () {
    // function to retrieve the "incorrect" letters
    return document.getElementById('wrong-letters').value.toLowerCase();
}

function removeIncorrectLetters (wrongVals) {
    // function to give letter possibilities with the "incorrect" letters removed
    // wrongvals is a string output from the getWrongLetterValues function
    
    // array of all letters
    const allLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'];

    // array to hold letters that are not "incorrect"
    lettersMinusInoccrectLetters = [];

    // loop through all letters and determine if they are "incorrect"; if not... add to array
    for (let letter of allLetters) {
        if (wrongVals.includes(letter) === false) {
            lettersMinusInoccrectLetters.push(letter);
        }
    }

    return lettersMinusInoccrectLetters;
}


function regexPositionPossibilites (wrongValsRemoved, correctLetterVals) {
    // function to map regex expressions for each index to the corresponding keys in an object
    // wrongValsRemoved is an array and is returned by removeIncorrectLetters function
    // correctLetterVals is an object and is returned by the getCorrectLetterValues function

    // object to hold regex expressions for each letter within the total word
    const letterPositionPossibilities = {
        1: '',
        2: '',
        3: '',
        4: '',
        5: ''
    };

    // loop through each key for each letter position
    for (let position of Object.keys(letterPositionPossibilities)) {
        // determine if the same key has a non empty string in correctLetterVals
        if (correctLetterVals[position]) {
            // map correct letter to the same key in the possible letters array
            letterPositionPossibilities[position] = correctLetterVals[position];
        } else {
            // if no correct letter for the key then map the letters that are not "incorrect" (wrongValsRemoved parameter)
            letterPositionPossibilities[position] = [];

            // loop through wrong vals and add them to positionpossibilities
            // this step avoids making all indices the same array which prevents modifying only a subset of arrays downstream...
            for (letter of wrongValsRemoved) {
                letterPositionPossibilities[position].push(letter);
            }
        }
    };
    
    return letterPositionPossibilities;
}


function removeMisplacedLetters (letterPositionPossibles, misplacedVals, misplacedValsPositions) {
    /*  function to remove misplaced letters as possible letters where they are known not to belong to
        letterPositionPossibles is an object returned by regexPositionPossiblities function
        misplacedVals is an object returned by the getMisplacedLetterValues function
        misplacedValsPositions is an object returned by the getMisplacedLetterIncorrectLetterPositions function
        *** all objects have the same keys ***
    */
    
    // loop through "misplaced" letters
    for (let position of Object.keys(misplacedVals)) {
        // if a key has a misplaced letter...
        if (misplacedVals[position]) {
            // capture value of misplaced letter (this is a string)
            let letterToRemove = misplacedVals[position];
            // capture letter positions where the misplaced letter is "incorrect" (this is an array)
            let positionsToRemoveFrom = misplacedValsPositions[position];
            
            // if positionsToRemoveFrom isn't empty...
            if (positionsToRemoveFrom.length !== 0){
                // loop through positionsToRemovedFrom (array)
                for (let positionToRemoveFrom of positionsToRemoveFrom) {
                    // determine if position is a single letter or an array that should be adjusted (have misplaced letter removed)
                    if (typeof(letterPositionPossibles[positionToRemoveFrom]) === 'object' ) {
                        // capture index of letter to be removed from array at appropriate key of letterPositionPossibles 
                        let removalIndex = letterPositionPossibles[positionToRemoveFrom].indexOf(letterToRemove);
                        // remove letter from array
                        letterPositionPossibles[positionToRemoveFrom].splice(removalIndex,1);
                    }
                
                }
            }
            
        }
    }

    return letterPositionPossibles;
}


function createFinalRegexExpression (letterPosPossibiles, misplacedVals) {
    /*  function that creates the regex expression for querying database
        letterPosPossibles is an object returned by removeMisplacedLetters function
        misplaecdVals is an object returned by the getMisplacedLetterValues function
    */

    // empty string to hold final regex expression
    let finalRegexExpression = '';

    // array to hold positive lookahead assertions
    let positiveLookAheadAssertions = [];

    // loop through misplaced letters
    for (let idx of Object.keys(misplacedVals)) {
        // if idx holds a misplaced letter...
        if (misplacedVals[idx]) {
            // initialize total instances of letter in the word as 1
            let totalLetterInstance = 1;
            // loop through letter possibilities
            for (let position of Object.keys(letterPosPossibiles)) {
                // if misplaced letter is also a "correct" letter in the word...
                if (misplacedVals[idx] === letterPosPossibiles[position]) {
                    // increment total instances of letter in the word
                    totalLetterInstance ++
                }
            }
            // if misplaced letter has only 1 known total instance...
            if (totalLetterInstance === 1) {
                // add the following assertion to assertion array
                positiveLookAheadAssertions.push(`(?=.*${misplacedVals[idx]}.*)`)
            }
            // if misplaced letter has 2 known instances... (misplaced and correct)
            if (totalLetterInstance === 2) {
                // add the following assertion to assertion array
                positiveLookAheadAssertions.push(`(?=.*${misplacedVals[idx]}.*${misplacedVals[idx]}.*)`)
            }
            // if misplaced letter has 3 known instances... (misplaced and 2 correct)
            if (totalLetterInstance === 3) {
                // add the following assertion to assertion array
                positiveLookAheadAssertions.push(`(?=.*${misplacedVals[idx]}.*${misplacedVals[idx]}.*${misplacedVals[idx]}.*)`)
            }
        }
    }

    // variable to hold regex expression (excepting the positive lookahead assertions)
    let addedPossiblities = ''

    // loop through letter positions
    for (let pos of Object.keys(letterPosPossibiles)) {
        // if letter possibility is a letter (string)...
        if (typeof(letterPosPossibiles[pos]) === 'string') {
            // add letter to the end of added possibilities
            addedPossiblities = addedPossiblities + letterPosPossibiles[pos];
        }
        // if letter possibility is an array of letters...
        if (typeof(letterPosPossibiles[pos]) === 'object') {
            // initialize string form of array
            let arrayToString = '';
            // loop through array and add letters to each other
            for (letter of letterPosPossibiles[pos]) {
                arrayToString = arrayToString + letter;
            }
            // add brackets to make letters into a regex character class
            addedPossiblities = addedPossiblities + '[' + arrayToString + ']';
        }
    }

    // loop through assertion is assertion array
    for (assertion of positiveLookAheadAssertions) {
        // add assertions to final regex expression
        finalRegexExpression = finalRegexExpression + assertion;
    }
    
    // add the two regex epressions together to get completed final expression
    finalRegexExpression = finalRegexExpression + addedPossiblities;

    return finalRegexExpression;
}