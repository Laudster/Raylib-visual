const codeblocks = {
    "Render": ["Change Background: (color)", "Draw Rectangle: (vector2) (color)", "Draw Text: (text) (vector2) (color)"],
    "Input": ["IsKeyDown: (keycode)", "IsMouseDown: (mousebutton)"],
    "Logic": ["If: (statement)", "Else", "Else If: (statement)"],
    "Loops": ["For: (statement)", "While: (statement)"],
    "Math": ["(number) + (number)", "(number) - (number)"],
    "Variables": ["Set variable", "Increase (variable) by (number)"]}

function update_panel(inner){
    document.getElementById("coding").firstElementChild.innerHTML = inner;

    document.getElementById("coding").innerHTML = "";
                    
    let newTitle = document.createElement("h2");
    newTitle.innerHTML = inner;
    document.getElementById("coding").appendChild(newTitle);

    codeblocks[inner].forEach(value =>{
        let codeblock = document.createElement("button");
        codeblock.innerHTML = value;
        document.getElementById("coding").appendChild(codeblock);
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