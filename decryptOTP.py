from collections import defaultdict

ciphertexts =  ['BB3A65F6F0034FA957F6A767699CE7FABA855AFB4F2B520AEAD612944A801E',
                'BA7F24F2A35357A05CB8A16762C5A6AAAC924AE6447F0608A3D11388569A1E',
                'A67261BBB30651BA5CF6BA297ED0E7B4E9894AA95E300247F0C0028F409A1E',
                'A57261F5F0004BA74CF4AA2979D9A6B7AC854DA95E305203EC8515954C9D0F',
                'BB3A70F3B91D48E84DF0AB702ECFEEB5BC8C5DA94C301E0BECD241954C831E',
                'A6726DE8F01A50E849EDBC6C7C9CF2B2A88E19FD423E0647ECCB04DD4C9D1E',
                'BC7570BBBF1D46E85AF9AA6C7A9CEFA9E9825CFD5E3A0047F7CD009305A71E']

clist = []
# Split the ciphertexts in pairs of 2, since these are 8 bit Hex numbers.
for i in range(len(ciphertexts)):
    clist.append([int(ciphertexts[i][j:j+2], 16) for j in range(0, len(ciphertexts[i]), 2)])

space_val = 32
stream = 0
dictposkeys = defaultdict(list)
# Loop through evert n'th byte at the same time, so we can compare them later...
for c0,c1,c2,c3,c4,c5,c6 in zip(clist[0],clist[1],clist[2],clist[3],clist[4],clist[5],clist[6]):
    all_cs = [c0,c1,c2,c3,c4,c5,c6]
    # The next two for loops make sure that we get all 21 combinations in which we can XOR the n'th bytes with eachother.
    for i in range(len(all_cs)-1):
        for j in range(i+1, len(all_cs)):
            xorval = all_cs[i]^all_cs[j]
            # If the last two bits are '01' then it is highly likely that one is a space character and the other a letter.
            if xorval > 63:
                # We then append the ID's of the two XORed ciphertexts that give '01' with the current stream number as its key value.
                dictposkeys[stream].append((i,j))
    # If none of the XORed texts gave any result for the curernt stream append some false result anyways 
    # so we can do something with it later
    if stream not in dictposkeys:
        dictposkeys[stream].append((len(clist),len(clist)))
    stream += 1

# For every stream we want to count how many times each ciphertext gave '01' as a result
# If a ciphertext contains a space character at a certain byte, then it will give '01' when matched with almost every other ciphertext.
# Then we know for sure that byte is a space character.
spacelist = []
for i in range(len(dictposkeys)):
    countdict = {}
    if len(dictposkeys[i]) > 0:
        for (a,b) in dictposkeys[i]:
            if a in countdict:
                countdict[a] += 1
            else:
                countdict[a] = 1
            if b in countdict:
                countdict[b] += 1
            else:
                countdict[b] = 1
        spacelist.append(max(countdict, key=countdict.get))
    else:
        spacelist.append('x')
# Create the first version of the key list by just XORing the space value with the found ciphered space character 
# in one of the ciphertexts to obtain the real key.
keylist = []
for i in range(len(spacelist)):
    if spacelist[i] == 'x':
        keylist.append(0)
    elif spacelist[i] == len(clist):
        keylist.append(0)
    else:
        keylist.append(space_val^clist[spacelist[i]][i])


# We know the last character is probably a period, so the key must be 1E XOR 2E = 30
keylist[30] = 48
# In ciphertext 0 the first two plaintext characters are probably "I" and "space", (because character 3 and 4 form the word 'am') 
# which correspond to the keys BB XOR 49 = F2 and 3A XOR 20 = 1A
keylist[0] = 242
keylist[1] = 26
# After the last step and replacing every unknown character with an 'X'
# it became clear that the 0th ciphertext is: 'I am planning a secret mission.'
# So the remaining keys are:
keylist[6] = 35
keylist[8] = 57
keylist[10] = 206
keylist[17] = 224
keylist[20] = 42
keylist[29] = 238

print(keylist)
# Decrypt every ciphertext
for k in range(len(clist)):
    m = ''
    for a,b in zip(clist[k],keylist):
        if chr(a^b).isalpha() or a^b == 46 or a^b == 63 or a^b == 39 or a^b == 32:
            m += chr(a^b)
        else:
            m += 'X' 
    print(m)


