const socket = io.connect(window.location.origin);

socket.on("connect", function(){
    console.log("connected");
});

socket.on("disconnect", function(){
    console.log("disconnected");
});

let projectLink = "";

let codeSection = "";

const codeblocks = {
    "Render": ["Draw Rectangle: (number) (number) (number) (number) (color)", "Draw Circle: (number) (number) (number) (color)", "Draw Text: (text) (number) (number) (number) (color)"],
    "Input": ["IsKeyDown: (keycode)", "IsMouseDown: (mousebutton)"],
    "Logic": ["If: (statement)", "Else", "Else If: (statement)", "And", "Or", "Not"],
    "Loops": ["Loop: (number)", "While: (statement)"],
    "Math": ["(number) + (number)", "(number) - (number)", "(number) * (number)", "(number) : (number)", "(number) == (number)", "(text) == (text)"],
    "Variables": ["Create variable: (assignvalue) (variable)", "Set variable: (thevariable) (value)"]}

let variables = {"defaultColour": "0x000000ff", "FPS": 60, "title": "Game"};

function isHex(inputString)
{
	var re = /[0-9A-Fa-f]{6}/g;

	if(re.test(inputString)) {
		return true
	} else {
		return false
	}
}

function highlight(color){
    ["setup", "input", "update", "render"].forEach(ting => {
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
    
        ["setup", "update", "input", "render"].forEach(stupid => {
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

        ["setup", "update", "input", "render"].forEach(stupid => {
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
            
        } else if (event.target.style.borderColor == "blue" && operatorBlock != "" && operatorBlock.innerHTML != "Not "){
            let newOperator = operatorBlock.cloneNode();
            newOperator.innerHTML = operatorBlock.innerHTML;
            event.target.parentElement.appendChild(newOperator);

            let newStatement = document.createElement("input");
            newStatement.type = "tel";
            newStatement.placeholder = "statement";
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

        ["Setup", "Input", "Update", "Render"].forEach(id => {
            document.getElementById(id).querySelector("button").style.backgroundColor = "";
        });

        button.style.backgroundColor = "rgb(200, 200, 200)";
    }
}

function processCodeblocks()
{
    let setup = [];
    for (const block of document.getElementById("setup").children){

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

        setup.push(line);
    }

    let input = [];
    for (const block of document.getElementById("input").children){

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
    for (const block of document.getElementById("update").children){

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
    for (const block of document.getElementById("render").children){

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

    return {"setup": setup, "input": input, "update": update, "render": render};
}

function add_variable_type(event)
{
    const newType = event.target.value;


    if (newType == "text")
    {
        let newInput = document.createElement("input");
        newInput.type = "text";
        newInput.placeholder = "text";
        newInput.addEventListener("mouseup", (event) => mouse_entered_input(event));


        event.target.parentElement.appendChild(newInput);
    }

    if (newType == "color")
        {
            let newInput = document.createElement("input");
            newInput.type = "color";
    
    
            event.target.parentElement.appendChild(newInput);
        }

    if (newType == "number")
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
    if (event.target.parentElement.querySelector("select").value == "text")
    {
        variables[event.target.value] = "";
        update_panel("Variables");
    } else if (event.target.parentElement.querySelector("select").value == "color"){
        variables[event.target.value] = "#000000";
        update_panel("Variables");

    } else if (event.target.parentElement.querySelector("select").value == "number")
    {
        variables[event.target.value] = 0;
        update_panel("Variables");
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
                variableInput.placeholder = "text";
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

    if (inner == "Variables")
    {
        Object.keys(variables).forEach(variable =>{
            let button = document.createElement("button");
            button.innerHTML = variable;
            button.style.display = "inline";

            button.onmousedown = () =>{
                variableSelelect = button.textContent;


                ["setup", "input", "update", "render"].forEach(ting => {
                    for (const block of document.getElementById(ting).children){
                        for (const element of block.children){
                            if (element.tagName == "INPUT") element.style.borderColor = "blue";
                        }
                    }
                })
            }

            button.onmouseup = () =>{
                variableSelelect = "";
                ["setup", "input", "update", "render"].forEach(ting => {
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
                                statement.placeholder = "statement"

                                li.appendChild(statement);
                            } else addons.push("statement");
                        } else if (word == "(text)"){
                            if (i == 0){
                                let text = document.createElement("input");
                                text.type = "text";
                                text.placeholder = "text"

                                li.appendChild(text);
                            } else addons.push("text");
                        } else if (word == "(variable)"){
                            if (i == 0){
                                let variable = document.createElement("input");
                                variable.type = "text";
                                variable.placeholder = "name"

                                li.appendChild(variable);
                            } else addons.push("variable");
                        } else if (word == "(keycode)"){
                            if (i == 0){
                                let selector = document.createElement("select")
                                selector.name = "options";

                                ["Space", "Arrow Up", "Arrow Down", "Arrow Left", "Arrow Right"].forEach(key =>{
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

                                ["Left", "Right", "Middle"].forEach(key =>{
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
                                defaultOpt.textContent = "variable";
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
                                defaultOpt.textContent = "value";
                                variablevalue.appendChild(defaultOpt);

                                ["text", "number", "color"].forEach(valuetype => {
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

        if (inner == "Math")
        {
                button.className = "short";

                if (button.textContent.replace(" ", "") != "=="){
                    button.onmousedown = () =>
                        {
                            mathBlock = button.parentElement;
        
                            ["setup", "input", "update", "render"].forEach(ting => {
                                for (const block of document.getElementById(ting).children){
                                    for (const element of block.children){
                                        if (element.tagName == "INPUT" && element.type == "number") element.style.borderColor = "blue";
                                    }
                                }
                            })
                        }
        
                        button.onmouseup = () => {
        
                            mathBlock = "";
        
                            ["setup", "input", "update", "render"].forEach(ting => {
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
            
                        ["setup", "input", "update", "render"].forEach(ting => {
                            for (const block of document.getElementById(ting).children){
                                for (const element of block.children){
                                    if (element.type == "tel") element.style.borderColor = "blue";
                                }
                            }
                        })
                    }
        
                    button.onmouseup = () =>{
                        keyBlock = "";
            
                        ["setup", "input", "update", "render"].forEach(ting => {
                            for (const block of document.getElementById(ting).children){
                                for (const element of block.children){
                                    if (element.type == "tel") element.style.borderColor = "";
                                }
                            }
                        })
                    }
                }
        }

        if (inner == "Input"){
            button.onmousedown = () =>{
                keyBlock = li;
    
                highlight("blue");
            }

            button.onmouseup = () =>{
                keyBlock = "";
    
                highlight("");
            }
        }

        if (inner == "Logic"){
            button.className = "condition";
            if (button.textContent != "Not " && button.textContent != "And " && button.textContent != "Or "){
                button.onclick = () => {
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
                                }
                            }

                            copy.remove();
                        }
                    })
    
                    copy.querySelector("input").addEventListener("mouseup", (event) => mouse_entered_input(event));
    
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

        if (inner == "Loops"){
            button.className = "condition";
        }
        
        if (inner == "Render"){
            button.onclick = () => {
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
                document.getElementById(codeSection).appendChild(copy);
            };
        }

        if (addons.includes("variable")){
            button.onclick = () => {
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

                document.getElementById(codeSection).appendChild(copy);
            };
        }

        if (addons.includes("thevariable")){
            button.onclick = () => {
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

                if (typeof(codeSection) !== "string"){
                    codeSection.parentElement.insertBefore(copy, codeSection.nextSibling);
                    copy.style.marginLeft = "5%";
                }
                else document.getElementById(codeSection).appendChild(copy);
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
                statement.placeholder = "statement";

                li.appendChild(statement);
            } else if (addon == "text"){
                let text = document.createElement("input");
                text.type = "text";
                text.placeholder = "text";
                

                li.appendChild(text);
            } else if (addon == "variable"){
                let variable = document.createElement("input");
                variable.type = "text";
                variable.placeholder = "name";

                li.appendChild(variable);
            } else if (addon == "keycode"){
                let selector = document.createElement("select")
                selector.name = "options";

                let option1 = document.createElement("option");
                option1.value = "value";
                option1.textContent = "value";
                selector.appendChild(option1);

                ["Space", "Arrow Up", "Arrow Down", "Arrow Left", "Arrow Right"].forEach(key =>{
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
                option1.textContent = "value";
                selector.appendChild(option1);

                ["Left", "Right", "Middle"].forEach(key =>{
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
                defaultOpt.textContent = "variable";
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
                defaultOpt.textContent = "value";
                variablevalue.appendChild(defaultOpt);

                ["text", "number", "color"].forEach(valuetype => {
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
    if (projectLink != "")
        {
            projectLink = "";
            document.getElementById("build").style.backgroundColor = "";
            document.getElementById("open").style.display = "none";
            socket.emit("shutdown");

            document.getElementById("display").children[0].remove();
        } else
        {
            document.getElementById("build").style.backgroundColor = "rgb(27, 240, 27, 0.7)";

            document.body.style.cursor = "wait";
            document.getElementById("build").style.cursor = "wait";

            socket.emit("build", processCodeblocks());
        }
}

function open_project()
{
    window.open(projectLink);
}

socket.on("build-finnished", function(link){
    let iframe = document.createElement("iframe");
    iframe.src = "http://localhost:8000/project.html";
    document.getElementById("display").appendChild(iframe);

    document.body.style.cursor = "";
    document.getElementById("build").style.cursor = "pointer";
    projectLink = link;
    document.getElementById("open").style.display = "block";
});