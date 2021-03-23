import os

# Initial facts
charnumber = 0
moduledirold = 'docs/source/modules/'
moduledirnew = 'docs/source/modules2/'




for filename in os.listdir(moduledirold):
    # Exclude index.rst as it has not the issue
    if filename != 'index.rst' and filename != '.keep':
        with open((moduledirold+filename), 'r') as rstfile:
            content = rstfile.readlines()
            # Search for the line below the Title Name through '+++'
            linenumber = [x for x in range(len(content)) if '+++' in content[x].lower()]
            for i in content[linenumber[0]-1]:
                charnumber = charnumber+1
                # Do the Magic and search for '--' and save newline with everything behind the --
                if content[linenumber[0]-1][charnumber] == '-' and content[linenumber[0]-1][charnumber+1] == '-':
                    newline = (content[linenumber[0]-1][23:(charnumber)]+'\n')
                    break 
            # Now change the file content Title with the newline 
            content[linenumber[0]-1] = newline
            charnumber=0
            # Write that to a new file
            with open((moduledirnew+filename), 'a') as rstfileout:
                for i in content:
                    rstfileout.write(i)
