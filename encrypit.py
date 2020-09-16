from itertools import cycle
# ciphered text in hex code
cipher = "F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7EFFD673BE4ACF7BE8923CAB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF5B9A7CFEDF3EB850D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE6BF0D138A84CC931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF9226BE5BDE3FF7DD21ED56CF71F5C036A94D963FF8D473A351CE3FE5DA3CB84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451D47EFD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47AF59232A35A9A7AE7D33FB85FCE7AF5923AA31EDB3FF7D33ABF52C33FF0D673A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA36ED68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC93FE5DA3CB859D26BB1C63CED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A85A963FF3C727ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44DDF3FF5D73EA250C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87AB1D021A255DF71B1C436BF479A7AF0C13AA14794"
cipher = "4576C64965DEAF6D87706D830B5EE48239CF7070830045EB9C2C9C656CD60A5FF89C28CF6576C21D0BEC822180666D83005FAD9A22CF7870D70C59EE8B3D9B317FCF0444FE9A6D8A677BD1105FE58723883F3EF4005FE5CE3987786D830A4AFD8F2F867D77D71007AD9A258A3168C21A5FAD832C857E6CCA1D52AD812BCF796BCE0845AD8D22827C6BCD0048EC9A24807F6D830859E8CE2C9A6571CE085FE48D2C837D67830045EA8B3E9B747A831E42F986229A653ED70859EA8B39867F798D4962EBCE04CF667FCD1D4EE9CE3980316DC60C0BF481389D317BCE0842E19D6D80633EDA065EFFCE3A86777B841A0BFD8622817432830847E1CE04CF797FD50C0BF9816D8B7E3ECA1A0BF89D28CF7870D70C59EE8B3D9B623083200BEE8F23CF767BD74952E29B3FCF7473C20047FEC26D9F706DD01E44FF8A3EC3316ECB0645E8CE3F8A7271D10D58A1CE2E9D747ACA1D0BEE8F3F8B623083200BE98123C8653ED40845F9CE39803172CA1F4EAD8723CF703ED00648E48B3996316ACB085FAD8A228A623ED7014EFE8B6D9C7E6CD74944EBCE39877870C41A05A3C06DA6317ACC4945E29A6D987070D7495FE2CE2186677B830045AD8F6D987E6CCF0D0BFA86289D743EC61F4EFF9739877870C44962AD8A22CF7070C74958EC976D86623ED10C48E29C298A7530833D43EC9A6D86623ECD065FAD9D2282746ACB0045EACE04CF7073831E42E1822481763ED7060BFE9B3D9F7E6CD74944FFCE2186677B831C45E98B3FC1"

# the ciphered text back to integers, so we can loop through each character
cipher = [int(cipher[i:i+2],16) for i in range(0, len(cipher), 2)]
# first find the length of the key
max_N_list = []
# given that the key is in range 1 to 13
for key_len in range(1,13):
    freqs = {}
    counter = 0
    # test each key length and count the frequency of each hex code
    for i in range(0,len(cipher),key_len):
        if cipher[i] in freqs:
            freqs[cipher[i]] += 1
        else:
            freqs[cipher[i]] = 1
        counter += 1
    sumsqr = 0
    # compute the summation of the frequency squared
    for key in freqs:
        sumsqr += (freqs[key]/counter)**2
    max_N_list.append((sumsqr,key_len))
# the right key length is the key length with the largest sum
N = max(max_N_list)[1]

# now the right key values have to be computed
key_list = []
# create N amount of streams, that have the same shift value
for i in range(N):
    key_found = False
    stream = []
    # add the i'th character of the cipheredtext to the current stream
    for val in range(i,len(cipher),N):
        stream.append(cipher[val])
    possiblekeys = {}
    longest_dict = [0,{}]
    # the key can take any value between 0 and 255 (ASCII)
    for key in range(0,255):
        key_dict = {}
        key_truthness = True
        # XOR every character in the stream with the current test key
        encrypted = [a ^ key for a in stream]
        # if the newly created list contains any illegal characters, drop the key as a possible key
        for encval in encrypted:
            if 48 <= encval <= 57 or not(32 <= encval <= 127):
                key_truthness = False
                break
        if key_truthness == True:
            for encval in encrypted:
                # collect all alphabetical characters and determine each frequency
                if 97 <= encval <= 122:                
                    if encval in key_dict:
                        key_dict[encval] += 1
                    else:
                        key_dict[encval] = 1
        if bool(key_dict):
            # the key_dictionary with the largest amount of unique alphabetical characters is selected
            if len(key_dict) > len(longest_dict[1]):
                longest_dict[1] = key_dict
                longest_dict[0] = key
    key_list.append(longest_dict[0])
            # we also tried using the english alphabet distribution, this did not work however

            # if max(key_dict, key=key_dict.get) == 101 and key_found == False:
            #     key_list.append(key)
            #     key_found = True
            # elif max(key_dict, key=key_dict.get) == 97 and key_found == False:
            #     key_list.append(key)
            #     key_found = True
            # elif max(key_dict, key=key_dict.get) == 114 and key_found == False:
            #     key_list.append(key)
            #     key_found = True

print(key_list)
# when using the found key_list it is clear that the second key must be changed from 29 to 31
true_keys = [186, 31, 145, 178, 83, 205, 62] # true keys for first ciphered text
true_keys2 = [17, 30, 163, 105, 43, 141, 238, 77, 239] # true keys for second ciphered text
message = "".join([chr(a ^ b) for (a,b) in zip(cipher,cycle(true_keys))])
print(message)
