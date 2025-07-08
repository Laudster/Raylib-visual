def setVariable(section, isInIfStatement, variables, codeblock, tabs):
    if "Sett Variabel" in codeblock:
        if isInIfStatement: beguneIf = True
        splits = codeblock.split(":")[1].split(";")
        if splits[1] in variables:
            if variables[splits[1]] == "text":
                name = splits[0].replace(" ", "")
                if isInIfStatement == True:
                    section += f"strcpy({name}, {splits[1]});"
                else:
                    section += f"\n" + '\t'*tabs + f"strcpy({name}, {splits[1]});"
            elif variables[splits[1]] == "number":
                value = ""
                for i in range(1, len(splits)):
                    value += splits[i]
                if isInIfStatement == True:
                    section += f"{splits[0]} = {value};"
                else:
                    section += f"\n" + '\t'*tabs + f"{splits[0]} = {value};"
            else:
                if isInIfStatement == True:
                    section += f"{splits[0]} = {splits[1]};"
                else:
                    section += f"\n" + '\t'*tabs + f"{splits[0]} = {splits[1]};"
        else:
            if variables[splits[0].replace(" ", "")] == "text":
                name = splits[0].replace(" ", "")
                if isInIfStatement == True:
                    section += f"strcpy({name}, \"{splits[1]}\");"
                else:
                    section += f"\n" + '\t'*tabs + f"strcpy({name}, \"{splits[1]}\");"
            elif variables[splits[0].replace(" ", "")] == "color":
                if isInIfStatement == True:
                    section += f"{splits[0]} = GetColor(0x{splits[1][1: len(splits[1])]}ff);"
                else:
                    section += f"\n" + '\t'*tabs + f"{splits[0]} = GetColor(0x{splits[1][1: len(splits[1])]}ff);"
            else:
                value = ""
                for i in range(1, len(splits)):
                    value += splits[i]

                if isInIfStatement == True:
                    section += f"\n" + '\t'*tabs + f"{splits[0]} = {value};"
                else:
                    section += f"\n" + '\t'*tabs + f"{splits[0]} = {value};"
    return section, isInIfStatement
