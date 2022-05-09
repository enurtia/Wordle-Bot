import numpy as np

#---------Load 5 letter words---------
words = np.loadtxt("PATH_OF_5_LETTER_WORDS_LIST.txt", dtype=str)
words = np.char.lower(words)

vowels = ["A", "E", "I", "O", "U"]
vowelsLower = np.char.lower(vowels)

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
alphabet = set(list(np.char.lower(alphabet)))
tries = 6

#---------Get max vowels word, randomly---------
vowelCounter = lambda word: np.count_nonzero([char in vowelsLower for char in set(word)])

maxNumVowels = vowelCounter(words.item(0))
maxNumVowelsIndices = np.array([0])

for i in range(len(words)):
    word = words.item(i)
    
    vowelCt = vowelCounter(word)
    if vowelCt > maxNumVowels:
        maxNumVowels = vowelCt
        maxNumVowelsIndices = np.array([i])
    elif vowelCt == maxNumVowels:
        maxNumVowelsIndices = np.append(maxNumVowelsIndices, i)

maxNumVowelsRandInd = maxNumVowelsIndices.item(np.random.randint(0, len(maxNumVowelsIndices)))
maxVowelsWord = words.item(maxNumVowelsRandInd)

print("Number of words: ", len(words))
print("Word with the most vowels: " + maxVowelsWord)
#--------------------------------------

lastWord = maxVowelsWord
greens = []
yellows = []

#Count letters in word
def letterCount(word, letter):
    return np.count_nonzero([letter == char for char in word])

#Get number of unique letters in a word
def getUniqueness(word):
    return len(set(list(word)))


#----------Filtering----------
yellowsMost = dict.fromkeys(alphabet)
yellowsLeast = yellowsMost.copy()
greenWord = "-----"

print("\n\nPlease enter every other letter as a hyphen: '-'")
while "-" in greenWord and tries > 0:
    greens += [input("Green: ")]
    yellows += [input("Yellow: ")]

    greenWord = greens[6 - tries]

    #For greys
    for i in range(5):
        char = lastWord[i]
        #If grey
        if char != greens[6 - tries][i] and char !=  yellows[6 - tries][i]:
            if char not in yellows[6 - tries] and char not in greenWord:
                #If does not have yellow or green, remove
                if char in alphabet:
                    alphabet.remove(char)
            else:
                #If grey char & has yellow char, we know word  contains at most #yellows + #greens
                    ct = letterCount(yellows[6 - tries], char)
                    if yellowsMost[char] is None or (yellowsMost[char] is not None and ct < yellowsMost[char]):
                        yellowsMost[char] = ct
                        
    #For yellows
    for i in range(5):
        char = yellows[6 - tries][i]
        #If yellow and no grey, we know (word not incl. greens) contains at least #yellows
        if char != "-" and char in alphabet:
            #Only overide dict if not already at most
            ct = letterCount(yellows[6 - tries], char)
            if yellowsLeast[char] is None or (yellowsLeast[char] is not None and ct > yellowsLeast[char]):
                yellowsLeast[char] = ct
                
                
                
    #Conform to Greens, using greenWord
    newWords = np.empty(0)
    for i in range(len(words)):
        word = words[i]
        
        skip = False
        for j in range(5):
            char = greenWord[j]
            if char != "-" and char != word[j]:
                skip = True
                break
        
        if not skip:
            newWords = np.append(newWords, word)
            
    words = newWords
    
    #Filter with bounds given by yellow and grey data
    newWords = np.empty(0)
    for i in range(len(words)):
        word = words[i]
        
        skip = False
        #Least Bound
        for j, (k, v) in enumerate(yellowsLeast.items()):
            if v is not None and (letterCount(word, k) < int(v)):
                skip = True
                break
        
        #Most Bound
        for j, (k, v) in enumerate(yellowsMost.items()):
            if v is not None and (letterCount(word, k) > (int(v) + letterCount(greenWord, k))):
                skip = True
                break
                
        #Ensure we use available letters
        for char in word:
            if char not in alphabet:
                skip = True
                break
        
        #Yellows should not be in the same spots
        for j in range(5):
            char = yellows[6 - tries][j]
            if char != "-" and char == word[j]:
                skip = True
                break
        
        if not skip:
            newWords = np.append(newWords, word)

    words = newWords
    tries -= 1
    
    #Get word that is most unique
    mostUnique = words.item(0)
    mostUniqueVal = getUniqueness(mostUnique)
    for i in range(len(words)):
        word = words[i]
        wordUniqueness = getUniqueness(word)
        if wordUniqueness > mostUniqueVal:
            mostUniqueVal = wordUniqueness
            mostUnique = word
        
    print("\nNumber of words left: ", len(words))
    print("Most Unique Word: ", mostUnique)
    lastWord = mostUnique
    #----------Filter Done----------
