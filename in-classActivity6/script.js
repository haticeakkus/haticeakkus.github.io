let button = document.getElementById("myButton");
let container = document.getElementById("container");
let clicks = 0;
let level = 1;
let timeout = 500;

let clickText = document.getElementById("click");
let levelText = document.getElementById("level");

button.addEventListener("mouseover", startMoving);

function startMoving() {
  setTimeout(moveButton, timeout);
}

function moveButton() {
  let randomX = Math.random() * (container.offsetWidth - button.offsetWidth);
  let randomY = Math.random() * (container.offsetHeight - button.offsetHeight);
  button.style.marginLeft = randomX + "px";
  button.style.marginTop = randomY + "px";
}

button.addEventListener("click", handleClick);

function handleClick() {
    
    clicks++;
    if (clicks === 3) {
        clicks = 0;
        level++;
        timeout -= 100;
        if (level > 1) {
        alert(`Congratulations! LEVEL UUUUUUUUPPP!! Level: ${level}`);
        return;
        }
        else if (level === 6) {
            alert("Congratulations! You've won the game!");
        return;
        }

    setTimeout(moveButton, timeout);
  }

  
}
