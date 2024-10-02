const socket = io.connect(window.location.origin);

socket.on("connect", function(){
    console.log("connected");
});

socket.on("disconnect", function(){
    console.log("disconnected");
});

let projectLink = "";

const codeblocks = {
    "Render": ["Clear Background: (color)", "Draw Rectangle: (number) (number) (number) (number) (color)", "Draw Text: (text) (vector2) (color)"],
    "Input": ["IsKeyDown: (keycode)", "IsMouseDown: (mousebutton)"],
    "Logic": ["If: (statement)", "Else", "Else If: (statement)"],
    "Loops": ["For: (statement)", "While: (statement)"],
    "Math": ["(number) + (number)", "(number) - (number)"],
    "Variables": ["Create variable (variable) (assignvalue)", "Set variable (thevariable) (number)", "(thevariable) Increase by (number)"]}

let variables = {"defaultColour": [255, 255, 255, 255], "FPS": 60, "title": "Game"};

function processCodeblocks()
{
    let input = [];
    for (const block of document.getElementById("render").children){

        let line = "";
        for (const child of block.children){
            if (child.textContent) line += child.textContent;
            if (child.value) line += child.value;
        }

        input.push(line);
    }

    let update = [];
    for (const block of document.getElementById("render").children){

        let line = "";
        for (const child of block.children){
            if (child.textContent) line += child.textContent;
            if (child.value) line += child.value;
        }

        update.push(line);
    }

    let render = [];
    for (const block of document.getElementById("render").children){

        let line = "";
        for (const child of block.children){
            if (child.textContent) line += child.textContent;
            if (child.value) line += child.value;
        }

        render.push(line);
    }

    return {"input": input, "update": update, "render": render};
}

function update_panel(inner)
{
    document.getElementById("coding").firstElementChild.innerHTML = inner;

    document.getElementById("coding").innerHTML = "";
                    
    let newTitle = document.createElement("h2");
    newTitle.innerHTML = inner;
    document.getElementById("coding").appendChild(newTitle);


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

                                li.appendChild(number);
                            } else addons.push("number");
                        } else if (word == "(statement)"){
                            if (i == 0){
                                let statement = document.createElement("input");
                                statement.type = "text";
                                statement.placeholder = "statement"

                                li.appendChild(statement);
                            } else addons.push("statement");
                        } else if (word == "(variable)"){
                            if (i == 0){
                                let variable = document.createElement("input");
                                variable.type = "text";
                                variable.placeholder = "variable"

                                li.appendChild(variable);
                            } else addons.push("variable");
                        } else if (word == "(keycode)" || word == "(mousebutton)" || word == "(thevariable)"){
                            if (i == 0){
                                let selector = document.createElement("select")
                                selector.name = "options";

                                let option1 = document.createElement("option");
                                option1.value = "Option1";
                                option1.textContent = "Option1";
                                selector.appendChild(option1);

                                let option2 = document.createElement("option");
                                option2.value = "option2";
                                option2.textContent = "option2";
                                selector.appendChild(option2);

                                li.appendChild(selector);
                            } else addons.push("option")
                        }
                    } else
                    {
                        message += word + " "
                    }
            }
        
        let button = document.createElement("button");
        button.innerHTML = message;
        button.onclick = (event) => {
            const copy = li.cloneNode(true);
            const copyButton = copy.querySelector('button');

            copyButton.onclick = () => copy.remove();
            document.getElementById(li.name).appendChild(copy);
        };

        li.appendChild(button);

        addons.forEach(addon =>{
            if (addon == "color"){
                let color = document.createElement("input");
                color.type = "color";

                li.appendChild(color);
            } else if (addon == "number"){
                let number = document.createElement("input");
                number.type = "number";

                li.appendChild(number);
            } else if (addon == "statement"){
                let statement = document.createElement("input");
                statement.type = "text";
                statement.placeholder = "statement";

                li.appendChild(statement);
            } else if (addon == "variable"){
                let variable = document.createElement("input");
                variable.type = "text";
                variable.placeholder = "variable";

                li.appendChild(variable);
            } else if (addon == "option"){
                let selector = document.createElement("select")
                selector.name = "options";

                let option1 = document.createElement("option");
                option1.value = "Option1";
                option1.textContent = "Option1";
                selector.appendChild(option1);

                let option2 = document.createElement("option");
                option2.value = "option2";
                option2.textContent = "option2";
                selector.appendChild(option2);

                li.appendChild(selector);
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
    document.body.style.cursor = "";
    document.getElementById("build").style.cursor = "pointer";
    projectLink = link;
    document.getElementById("open").style.display = "block";
});