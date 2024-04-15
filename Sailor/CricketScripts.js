let dropZone = document.getElementById('drop_zone');
let imageContainer = document.getElementById('image_container');
let clearButton = document.getElementById('clear_button');

// Add dragover and drop event listeners
dropZone.addEventListener('dragover', handleDragOver, false);
dropZone.addEventListener('drop', handleFileSelect, false);
dropZone.addEventListener('click', handleFileClick, false);
clearButton.addEventListener('click', handleClearClick, false);

function handleDragOver(e) {
    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy'; 
    dropZone.classList.add('dragover');
}

function handleFileSelect(e) {
    e.stopPropagation();
    e.preventDefault();
    dropZone.classList.remove('dragover');
    console.log("File selected");

    let files = e.dataTransfer ? e.dataTransfer.files : e.target.files;
    if (files.length > 0) {
        let file = files[0];
        let reader = new FileReader();

        reader.onloadend = function() {
            let base64data = reader.result.replace('data:' + file.type + ';base64,', '');
            fetch('http://127.0.0.1:5500/Sailor/cricketFile.html', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image: base64data })
            })
            .then(response => response.json())
            .then(data => {
                let img = document.createElement('img');
                img.src = 'data:image/jpeg;base64,' + data.image;
                imageContainer.appendChild(img);
            });
        }

        reader.readAsDataURL(file);
    }
}

function handleFileClick() {
    console.log("File selected");

    let fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.addEventListener('change', handleFileSelect, false);
    fileInput.click();
}

function handleClearClick() {
    imageContainer.innerHTML = '';
}