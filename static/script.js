const socket = io.connect(window.location.origin);

socket.on("connect", function(){
    console.log("connected");
});

socket.on("disconnect", function(){
    console.log("disconnected");
});

let codeSection = "";

const codeblocks = {
    "Visuellt": ["Tegn Firkant: (number) (number) (number) (number) (color)", "Tegn Sirkel: (number) (number) (number) (color)", "Skriv Tekst: (text) (number) (number) (number) (color)"],
    "Inndata": ["Knapp Trykket: (keycode)", "Museknapp Nede: (mousebutton)", "MusePosisjonX", "MusePosisjonY"],
    "Logikk": ["Hvis: (statement)", "Ellers Om: (statement)", "Ellers", "Og", "Eller"],
    "Løkker": ["Gjenta: (number)", "Så Lenge: (statement)"],
    "Matte": ["(number) + (number)", "(number) - (number)", "(number) * (number)", "(number) : (number)", "(number) 🎲 (number)", "(number) == (number)", "(number) != (number)", "(number) < (number)", "(number) > (number)"],
    "Variabler": ["Lag Variabel: (assignvalue) (variable)", "Sett Variabel: (thevariable) (value)"]}

let variables = {"bakgrunnFarge": "0x000000ff", "FPS": 60, "tittel": "Spill"};

function isHex(inputString)
{
	var re = /[0-9A-Fa-f]{6}/g;

	if(re.test(inputString)) {
		return true
	} else {
		return false
	}
}

function addtocode(copy){
    console.log(codeSection);
    if (typeof(codeSection) !== "string"){
        let stillIfs = true;
        let sibling = codeSection.nextSibling;

        let isLast = false;

        if (sibling){
            for (let child of codeSection.parentElement.children){
                if (child.querySelector("button").textContent == codeSection.textContent){
                    if (child == codeSection) isLast = true
                    else isLast = false;
                }
            }

            while (stillIfs == true){
                let nextSibling = sibling.nextSibling;

        
                if (sibling.style.marginLeft == "5%"){
                    if (nextSibling){
                        if (nextSibling.querySelector("button").textContent != "If") sibling = nextSibling;
                    }
                } else stillIfs = false;
        
                if (!nextSibling) stillIfs = false;
            }
        }

        if (sibling != null){
            console.log(isLast);
            if (isLast == false) codeSection.parentElement.insertBefore(copy, sibling);
            else codeSection.parentElement.insertBefore(copy, sibling.nextSibling);
        }
        else codeSection.parentElement.insertBefore(copy, codeSection.nextSibling);
        copy.style.marginLeft = "5%";
    }
    else document.getElementById(codeSection).appendChild(copy);    
}

function highlight(color){
    ["start", "inndata", "oppdater", "visuelt"].forEach(ting => {
        for (const block of document.getElementById(ting).children){
            for (const element of block.children){
                if (element.type == "tel") element.style.borderColor = color;
            }
        }
    })
}

let variableSelelect = "";

let mathBlock = "";

let keyBlock = "";

let operatorBlock = "";

function mouse_entered_input(event)
{
    if (event.target.style.borderColor == "blue" && variableSelelect != ""){
        let variablebutton = document.createElement("button");
        variablebutton.textContent = variableSelelect;

        variableSelelect = "";

        event.target.parentElement.insertBefore(variablebutton, event.target);

        event.target.remove();
    
        ["start", "inndata", "oppdater", "visuelt"].forEach(stupid => {
            for (const block of document.getElementById(stupid).children){
                for (const element of block.children){
                    if (element.tagName == "INPUT") element.style.borderColor = "";
                }
            }
        })
    } else if (event.target.style.borderColor == "blue" && mathBlock != "")
    {
        for (const child of mathBlock.children){
            let copy = child.cloneNode();
            copy.innerHTML = child.innerHTML;
            
            if (copy.tagName == "INPUT"){
                copy.addEventListener("mouseup", (event) => mouse_entered_input(event));
            }

            event.target.parentElement.insertBefore(copy, event.target);
        }
        event.target.remove();

        mathBlock = "";

        ["start", "inndata", "oppdater", "visuelt"].forEach(stupid => {
            for (const block of document.getElementById(stupid).children){
                for (const element of block.children){
                    if (element.tagName == "INPUT") element.style.borderColor = "";
                }
            }
        })
        
    } else if (event.target.style.borderColor == "blue" && keyBlock != "")
        {
            for (const child of keyBlock.children){
                let copy = child.cloneNode();
                copy.innerHTML = child.innerHTML;
                
                if (copy.tagName == "INPUT"){
                    copy.addEventListener("mouseup", (event) => mouse_entered_input(event));
                }
                
                event.target.style.width = "1%";
                event.target.placeholder = "";
    
                event.target.parentElement.insertBefore(copy, event.target);
            }
    
            keyBlock = "";
    
            highlight("");
            
        } else if (event.target.style.borderColor == "blue" && operatorBlock != "" && operatorBlock.innerHTML != "Ikke "){
            let newOperator = operatorBlock.cloneNode();
            newOperator.innerHTML = operatorBlock.innerHTML;
            event.target.parentElement.appendChild(newOperator);

            let newStatement = document.createElement("input");
            newStatement.type = "tel";
            newStatement.placeholder = "påstand";
            newStatement.addEventListener("mouseup", (event) => mouse_entered_input(event));
            event.target.parentElement.appendChild(newStatement)

            if (event.target.placeholder == "") event.target.remove();

            operatorBlock = "";
            highlight("");
        } else if (event.target.style.borderColor == "blue" && operatorBlock.innerHTML != ""){
            let newOperator = operatorBlock.cloneNode();
            newOperator.innerHTML = operatorBlock.innerHTML;
            event.target.parentElement.insertBefore(newOperator, event.target);

            operatorBlock = "";
            highlight("");
        }
}
 

function chosen_section(button)
{
    if (codeSection == button.textContent.charAt(1).toLowerCase() + button.textContent.slice(2).replace(" ", ""))
    {
        document.getElementById(codeSection[0].toUpperCase() + codeSection.slice(1)).querySelector("button").style.backgroundColor = "";

        codeSection = "";
    } else
    {
        if (typeof(codeSection) !== "string") codeSection.querySelector("button").style.backgroundColor = "";
        codeSection = button.textContent.charAt(1).toLowerCase() + button.textContent.slice(2).replace(" ", "");

        ["Start", "Inndata", "Oppdater", "Visuelt"].forEach(id => {
            document.getElementById(id).querySelector("button").style.backgroundColor = "";
        });

        button.style.backgroundColor = "rgb(200, 200, 200)";
    }
}

function processCodeblocks()
{
    let start = [];
    for (const block of document.getElementById("start").children){

        let line = "";

        if (block.style.marginLeft == "5%") line += "tab";
        for (const child of block.children){
            if (child.textContent && child.tagName != "SELECT")
            {
                if (child.textContent in variables)
                {
                    line += child.textContent + ";";
                } else
                {
                    line += child.textContent;
                }
            }
            if (child.value) line += child.value + ";";
        }

        start.push(line);
    }

    let input = [];
    for (const block of document.getElementById("inndata").children){

        let line = "";

        if (block.style.marginLeft == "5%") line += "tab";
        for (const child of block.children){
            if (child.textContent && child.tagName != "SELECT")
            {
                if (child.textContent in variables)
                {
                    line += child.textContent + ";";
                } else
                {
                    line += child.textContent;
                }
            }
            if (child.value) line += child.value + ";";
        }

        input.push(line);
    }

    let update = [];
    for (const block of document.getElementById("oppdater").children){

        let line = "";

        if (block.style.marginLeft == "5%") line += "tab";
        for (const child of block.children){
            if (child.textContent && child.tagName != "SELECT")
            {
                if (child.textContent in variables)
                {
                    line += child.textContent + ";";
                } else
                {
                    line += child.textContent;
                }
            }
            if (child.value) line += child.value + ";";
        }

        update.push(line);
    }

    let render = [];
    for (const block of document.getElementById("visuelt").children){

        let line = "";

        if (block.style.marginLeft == "5%") line += "tab";
        for (const child of block.children){
            if (child.textContent && child.tagName != "SELECT")
            {
                if (child.textContent in variables)
                {
                    line += child.textContent + ";";
                } else
                {
                    line += child.textContent;
                }
            }
            if (child.value) line += child.value + ";";
        }

        render.push(line);
    }

    console.log({"setup": start, "input": input, "update": update, "render": render});

    return {"setup": start, "input": input, "update": update, "render": render};
}

function add_variable_type(event)
{
    const newType = event.target.value;


    if (newType == "tekst")
    {
        let newInput = document.createElement("input");
        newInput.type = "text";
        newInput.placeholder = "tekst";
        newInput.addEventListener("mouseup", (event) => mouse_entered_input(event));


        event.target.parentElement.appendChild(newInput);
    }

    if (newType == "farge")
        {
            let newInput = document.createElement("input");
            newInput.type = "color";
    
    
            event.target.parentElement.appendChild(newInput);
        }

    if (newType == "nummer")
    {
        let newInput = document.createElement("input");
        newInput.type = "number";
        newInput.value = 0;
        newInput.addEventListener("mouseup", (event) => mouse_entered_input(event));
    
        event.target.parentElement.appendChild(newInput);
    }
}

function add_variable(event)
{
    if (event.target.parentElement.querySelector("select").value == "tekst")
    {
        variables[event.target.value] = "";
        update_panel("Variabler");
    } else if (event.target.parentElement.querySelector("select").value == "farge"){
        variables[event.target.value] = "#000000";
        update_panel("Variabler");

    } else if (event.target.parentElement.querySelector("select").value == "nummer")
    {
        variables[event.target.value] = 0;
        update_panel("Variabler");
    }
}

function chosen_set_variable(event)
{

    if (event.target.parentElement.querySelector("input")) event.target.parentElement.querySelector("input").remove();

    if (event.target.value != "variable")
    {
        if (typeof(variables[event.target.value]) == "string")
        {

            if (isHex(variables[event.target.value]) == true){
                let variableInput = document.createElement("input");
                variableInput.type = "color";
                variableInput.onmouseup = (event) => mouse_entered_input(event);
                
                event.target.parentElement.appendChild(variableInput);
            } else{

                let variableInput = document.createElement("input");
                variableInput.type = "text";
                variableInput.placeholder = "tekst";
                variableInput.onmouseup = (event) => mouse_entered_input(event);
                
                event.target.parentElement.appendChild(variableInput);
            }
        } else if (typeof(variables[event.target.value]) == "number")
        {
            let variableInput = document.createElement("input");
            variableInput.type = "number";
            variableInput.value = 0;
            variableInput.onmouseup = (event) => mouse_entered_input(event);
                
            event.target.parentElement.appendChild(variableInput);
        }
    }
}

function update_panel(inner)
{
    document.getElementById("coding").firstElementChild.innerHTML = inner;

    document.getElementById("coding").innerHTML = "";
                    
    let newTitle = document.createElement("h2");
    newTitle.innerHTML = inner;
    document.getElementById("coding").appendChild(newTitle);

    if (inner == "Variabler")
    {
        Object.keys(variables).forEach(variable =>{
            let button = document.createElement("button");
            button.innerHTML = variable;
            button.style.display = "inline";

            button.onmousedown = () =>{
                variableSelelect = button.textContent;


                ["start", "inndata", "oppdater", "visuelt"].forEach(ting => {
                    for (const block of document.getElementById(ting).children){
                        for (const element of block.children){
                            if (element.tagName == "INPUT") element.style.borderColor = "blue";
                        }
                    }
                })
            }

            button.onmouseup = () =>{
                variableSelelect = "";
                ["start", "inndata", "oppdater", "visuelt"].forEach(ting => {
                    for (const block of document.getElementById(ting).children){
                        for (const element of block.children){
                            if (element.tagName == "INPUT") element.style.borderColor = "";
                        }
                    }
                })
            }

            document.getElementById("coding").appendChild(button);
        });
    }

    codeblocks[inner].forEach(codeblock => {
        let ul = document.createElement("ul");
        let splitcode = codeblock.split(" ");

        let message = "";
        let addons = [];

        let li = document.createElement("li");
        li.name = inner.toLowerCase();

        for (let i = 0; i < splitcode.length; i++)
            {
                word = splitcode[i];

                if (word[0] == "(")
                    {
                        if (word == "(color)"){
                            if (i == 0){
                                let color = document.createElement("input");
                                color.type = "color";

                                li.appendChild(color);
                            } else addons.push("color");
                        } else if (word == "(number)"){
                            if (i == 0){
                                let number = document.createElement("input");
                                number.type = "number";
                                number.value = 0;

                                li.appendChild(number);
                            } else addons.push("number");
                        } else if (word == "(statement)"){
                            if (i == 0){
                                let statement = document.createElement("input");
                                statement.type = "text";
                                statement.placeholder = "påstand"

                                li.appendChild(statement);
                            } else addons.push("statement");
                        } else if (word == "(text)"){
                            if (i == 0){
                                let text = document.createElement("input");
                                text.type = "text";
                                text.placeholder = "tekst"

                                li.appendChild(text);
                            } else addons.push("text");
                        } else if (word == "(variable)"){
                            if (i == 0){
                                let variable = document.createElement("input");
                                variable.type = "text";
                                variable.placeholder = "navn"

                                li.appendChild(variable);
                            } else addons.push("variable");
                        } else if (word == "(keycode)"){
                            if (i == 0){
                                let selector = document.createElement("select")
                                selector.name = "options";

                                ["Mellomrom", "Pil Opp", "Pil Ned", "Pil Venstre", "Pil Høyre"].forEach(key =>{
                                    let option1 = document.createElement("option");
                                    option1.value = key;
                                    option1.textContent = key;
                                    selector.appendChild(option1);
                                })

                                li.appendChild(selector);
                            } else addons.push("keycode")
                        } else if (word == "(mousebutton)"){
                            if (i == 0){
                                let selector = document.createElement("select")
                                selector.name = "options";

                                ["Venstre", "Høyre", "Midt"].forEach(key =>{
                                    let option1 = document.createElement("option");
                                    option1.value = key;
                                    option1.textContent = key;
                                    selector.appendChild(option1);
                                })

                                li.appendChild(selector);
                            } else addons.push("mousebutton");
                        } else if (word == "(thevariable)"){
                            if (i == 0){
                                let thevariable = document.createElement("select");
                                thevariable.name = "variable";;

                                let defaultOpt = document.createElement("option");
                                defaultOpt.value = "variable";
                                defaultOpt.textContent = "variabel";
                                thevariable.appendChild(defaultOpt);

                                Object.keys(variables).forEach(variable => {
                                    let option = document.createElement("option");
                                    option.value = variable;
                                    option.textContent = variable;
                                    thevariable.appendChild(option);
                                })

                                li.appendChild(thevariable);
                            } else addons.push("thevariable");
                        } else if (word == "(assignvalue)"){
                            if (i == 0){
                                let variablevalue = document.createElement("select");
                                variablevalue.name = "value";

                                let defaultOpt = document.createElement("option");
                                defaultOpt.value = "value";
                                defaultOpt.textContent = "verdi";
                                variablevalue.appendChild(defaultOpt);

                                ["tekst", "nummer", "farge"].forEach(valuetype => {
                                    let option = document.createElement("option");
                                    option.value = valuetype;
                                    option.textContent = valuetype;
                                    variablevalue.appendChild(option);
                                })

                                li.appendChild(variablevalue);
                            } else addons.push("variablevalue");
                        }
                    } else
                    {
                        message += word + " "
                    }
            }
        
        let button = document.createElement("button");
        button.innerHTML = message;

        if (inner == "Matte")
        {
                button.className = "short";

                if (button.textContent.replace(" ", "") != "==" && button.textContent.replace(" ", "") != "<" && button.textContent.replace(" ", "") != ">" && button.textContent.replace(" ", "") != "!="){
                    button.onmousedown = () =>
                        {
                            mathBlock = button.parentElement;
        
                            ["start", "inndata", "oppdater", "visuelt"].forEach(ting => {
                                for (const block of document.getElementById(ting).children){
                                    for (const element of block.children){
                                        if (element.tagName == "INPUT" && element.type == "number") element.style.borderColor = "blue";
                                    }
                                }
                            })
                        }
        
                        button.onmouseup = () => {
        
                            mathBlock = "";
        
                            ["start", "inndata", "oppdater", "visuelt"].forEach(ting => {
                                for (const block of document.getElementById(ting).children){
                                    for (const element of block.children){
                                        if (element.tagName == "INPUT" && element.type == "number") element.style.borderColor = "";
                                    }
                                }
                            })
                        }
                } else
                {
                    button.onmousedown = () =>{
                        keyBlock = li;
            
                        ["start", "inndata", "oppdater", "visuelt"].forEach(ting => {
                            for (const block of document.getElementById(ting).children){
                                for (const element of block.children){
                                    if (element.type == "tel") element.style.borderColor = "blue";
                                }
                            }
                        })
                    }
        
                    button.onmouseup = () =>{
                        keyBlock = "";
            
                        ["start", "inndata", "oppdater", "visuelt"].forEach(ting => {
                            for (const block of document.getElementById(ting).children){
                                for (const element of block.children){
                                    if (element.type == "tel") element.style.borderColor = "";
                                }
                            }
                        })
                    }
                }
        }

        if (inner == "Inndata"){
            if (button.innerHTML.search("Posisjon") > 0){
                button.className = "medium"

                button.onmousedown = () =>
                {
                    mathBlock = button.parentElement;

                    ["start", "inndata", "oppdater", "visuelt"].forEach(ting => {
                        for (const block of document.getElementById(ting).children){
                            for (const element of block.children){
                                if (element.tagName == "INPUT" && element.type == "number") element.style.borderColor = "blue";
                                if (element.tagName == "INPUT" && element.type == "text") element.style.borderColor = "blue";
                            }
                        }
                    })
                }

                button.onmouseup = () => {

                    mathBlock = "";

                    ["start", "inndata", "oppdater", "visuelt"].forEach(ting => {
                        for (const block of document.getElementById(ting).children){
                            for (const element of block.children){
                                if (element.tagName == "INPUT" && element.type == "number") element.style.borderColor = "";
                                if (element.tagName == "INPUT" && element.type == "text") element.style.borderColor = "";
                            }
                        }
                    })
                }
            } else {
                button.onmousedown = () =>{
                    keyBlock = li;
        
                    highlight("blue");
                }

                button.onmouseup = () =>{
                    keyBlock = "";
        
                    highlight("");
                }
            }
        }

        if (inner == "Logikk"){
            button.className = "condition";
            if (button.textContent != "Ikke " && button.textContent != "Og " && button.textContent != "Eller "){
                button.onmousedown = () => {
                    const copy = li.cloneNode(true);
    
                    copy.querySelector('button').addEventListener("mousedown", function(event){
                        event.preventDefault();
                        if (event.button == 0)
                        {
                            if (typeof(codeSection) == "string" && codeSection != ""){
                                document.getElementById(codeSection[0].toUpperCase() + codeSection.slice(1)).querySelector("button").style.backgroundColor = "";
                            } else if (codeSection != "") codeSection.querySelector("button").style.backgroundColor = "";
                            copy.querySelector("button").style.backgroundColor = "rgb(200, 200, 200)";
                            codeSection = copy;
                        }
                        if (event.button == 1){

                            if (copy.nextSibling){
                                let stillIfs = true;
                                let sibling = copy.nextSibling;

                                while (stillIfs == true){
                                    let nextSibling = sibling.nextSibling;

                                    if (sibling.style.marginLeft == "5%"){
                                        sibling.remove();
                                        sibling = nextSibling;
                                    } else stillIfs = false;

                                    if (!nextSibling) stillIfs = false;
                                }
                            }

                            copy.remove();
                        }
                    })
    
                    if (copy.querySelector("input")) copy.querySelector("input").addEventListener("mouseup", (event) => mouse_entered_input(event));
    
                    document.getElementById(codeSection).appendChild(copy);
                };
            } else{
                button.onmousedown = () => {
                    operatorBlock = button;
                    highlight("blue");
                }

                button.onmouseup = () => {
                    operatorBlock = "";
                    highlight("");
                }
            }
        }

        if (inner == "Løkker"){
            button.className = "condition";

            button.onmousedown = () => {
                const copy = li.cloneNode(true);
    
                copy.querySelector('button').addEventListener("mousedown", function(event){
                    event.preventDefault();
                    if (event.button == 0)
                    {
                        if (typeof(codeSection) == "string" && codeSection != ""){
                            document.getElementById(codeSection[0].toUpperCase() + codeSection.slice(1)).querySelector("button").style.backgroundColor = "";
                        } else if (codeSection != "") codeSection.querySelector("button").style.backgroundColor = "";
                        copy.querySelector("button").style.backgroundColor = "rgb(200, 200, 200)";
                        codeSection = copy;
                    }
                    if (event.button == 1){

                        if (copy.nextSibling){
                            let stillIfs = true;
                            let sibling = copy.nextSibling;

                            while (stillIfs == true){
                                let nextSibling = sibling.nextSibling;

                                if (sibling.style.marginLeft == "5%"){
                                    sibling.remove();
                                    sibling = nextSibling;
                                } else stillIfs = false;

                                if (!nextSibling) stillIfs = false;
                            }
                        }

                        copy.remove();
                    }
                })
    
                if (copy.querySelector("input")) copy.querySelector("input").addEventListener("mouseup", (event) => mouse_entered_input(event));
    
                document.getElementById(codeSection).appendChild(copy);
            };
        }
        
        if (inner == "Visuellt"){
            button.onmousedown = () => {
                const copy = li.cloneNode(true);
    
                for (const c of copy.children)
                {
                    if (c.tagName == "INPUT"){
                        c.addEventListener("mouseup", (event) => mouse_entered_input(event));
                    }
                }

                copy.querySelector('button').addEventListener("mousedown", function(event){
                    event.preventDefault();
                    if (event.button == 1) copy.remove();
                })

                addtocode(copy);
            };
        }

        if (addons.includes("variable")){
            button.onmousedown = () => {
                const copy = li.cloneNode(true);

                for (const c of copy.children)
                {
                    if (c.tagName == "INPUT"){
                        c.addEventListener("mouseup", (event) => mouse_entered_input(event));
                    }
                }
                
                copy.querySelector("select").addEventListener("change", event => add_variable_type(event));
                copy.querySelector("input").addEventListener("change", event => add_variable(event));
                copy.querySelector('button').addEventListener("mousedown", function(event){
                    event.preventDefault();
                    if (event.button == 1) copy.remove();
                })

                addtocode(copy);
            };
        }

        if (addons.includes("thevariable")){
            button.onmousedown = () => {
                const copy = li.cloneNode(true);

                for (const c of copy.children)
                {
                    if (c.tagName == "INPUT"){
                        c.addEventListener("mouseup", (event) => mouse_entered_input(event));
                    }
                }

                copy.querySelector("select").addEventListener("change", event => chosen_set_variable(event));
                copy.querySelector('button').addEventListener("mousedown", function(event){
                    event.preventDefault();
                    if (event.button == 1) copy.remove();
                })

                addtocode(copy);
            };
        }

        li.appendChild(button);

        addons.forEach(addon =>{
            if (addon == "color"){
                let color = document.createElement("input");
                color.type = "color";

                li.appendChild(color);
            } else if (addon == "number"){
                let number = document.createElement("input");
                number.type = "number";
                number.value = 0;

                li.appendChild(number);
            } else if (addon == "statement"){
                let statement = document.createElement("input");
                statement.type = "tel";
                statement.placeholder = "påstand";

                li.appendChild(statement);
            } else if (addon == "text"){
                let text = document.createElement("input");
                text.type = "text";
                text.placeholder = "tekst";
                

                li.appendChild(text);
            } else if (addon == "variable"){
                let variable = document.createElement("input");
                variable.type = "text";
                variable.placeholder = "navn";

                li.appendChild(variable);
            } else if (addon == "keycode"){
                let selector = document.createElement("select")
                selector.name = "options";

                let option1 = document.createElement("option");
                option1.value = "value";
                option1.textContent = "verdi";
                selector.appendChild(option1);

                ["Mellomrom", "Pil Opp", "Pil Ned", "Pil Venstre", "Pil Høyre"].forEach(key =>{
                    let option1 = document.createElement("option");
                    option1.value = key;
                    option1.textContent = key;
                    selector.appendChild(option1);
                })

                li.appendChild(selector);
            } else if (addon == "mousebutton"){
                let selector = document.createElement("select")
                selector.name = "options";

                let option1 = document.createElement("option");
                option1.value = "value";
                option1.textContent = "verdi";
                selector.appendChild(option1);

                ["Venstre", "Høyre", "Midt"].forEach(key =>{
                    let option = document.createElement("option");
                    option.value = key;
                    option.textContent = key;
                    selector.appendChild(option);
                })

                li.appendChild(selector);
            } else if (addon == "thevariable"){
                let thevariable = document.createElement("select")
                thevariable.name = "variable";;

                let defaultOpt = document.createElement("option");
                defaultOpt.value = "variable";
                defaultOpt.textContent = "variabel";
                thevariable.appendChild(defaultOpt);

                Object.keys(variables).forEach(variable => {
                    let option = document.createElement("option");
                    option.value = variable;
                    option.textContent = variable;
                    thevariable.appendChild(option);
                })

                li.appendChild(thevariable);
            } else if (addon == "variablevalue"){
                let variablevalue = document.createElement("select");
                variablevalue.name = "value";

                let defaultOpt = document.createElement("option");
                defaultOpt.value = "value";
                defaultOpt.textContent = "verdi";
                variablevalue.appendChild(defaultOpt);

                ["tekst", "nummer", "farge"].forEach(valuetype => {
                    let option = document.createElement("option");
                    option.value = valuetype;
                    option.textContent = valuetype;
                    variablevalue.appendChild(option);
                })

                li.appendChild(variablevalue)
            }
        });

        ul.appendChild(li);
        document.getElementById("coding").appendChild(ul);

    });
    
}

function show_codes(button)
{
    if (document.getElementById("coding").style.display != "block")
        {
            document.getElementById("coding").style.display = "block";
            update_panel(button.innerHTML.trim());
        } else if(button.innerHTML.trim() == document.getElementById("coding").firstChild.innerHTML.trim())
        {
            document.getElementById("coding").style.display = "none";
        } else
        {
            document.getElementById("coding").style.display = "block";
            update_panel(button.innerHTML.trim());
        }
}

function build_project()
{
    document.getElementById("build").backgroundColor = "rgb(27, 240, 27, 0.7)";
    socket.emit("build", processCodeblocks());

    socket.emit("getSessId", function(sessID){
        console.log(sessID);
        window.open("raylibvisual://" + sessID, "_parent");
    });
}

socket.on("build-finnished", function(){
    let iframe = document.createElement("iframe");
    iframe.src = "http://localhost:8001/project.html";
    document.getElementById("display").appendChild(iframe);
});

socket.on("quit", function(){
    console.log("remove");
    document.getElementById("display").querySelector("iframe").remove();
    document.getElementById("build").backgroundColor = "";
});