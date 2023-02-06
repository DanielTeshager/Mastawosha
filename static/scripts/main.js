//define the variables
var submit = document.getElementById("submit");

//get the date from the web server using vanilla js
function getNotes() {
	//fetch the data from the server
	fetch("/")
		.then(function (response) {
			return response.json();
		})
		.then(function (data) {
			//console.log(data);
			allNotes = data;
			console.log(allNotes);
			//console.log(allNotes);
			return allNotes;
		})
		.catch(function (error) {
			console.log(error);
		});
}

//alert when the page loads
window.onload = function () {
	//populate the notes on the page
	// populateNotes();
	getNotes();
};

submit.addEventListener("click", function (event) {
	//prevent the default behaviour of the form
	event.preventDefault();
	//get the data from the form
	let title = document.getElementById("title").value;
	let description = document.getElementById("desrciption").value;
	let image = document.getElementById("image").value;
	let tags = document.getElementById("tags").value;
	let link = document.getElementById("link").value;

	//validate the data
	if (
		title == "" ||
		description == "" ||
		tags == "" ||
		image == "" ||
		link == ""
	) {
		alert("Please fill all the fields");
	} else {
		//send the data to the server
		fetch("/notes/new", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				crossDomain: true,
				"Access-Control-Allow-Origin": "*",
			},
			body: JSON.stringify({
				title: title,
				description: description,
				image: image,
				tags: tags,
				link: link,
			}),
		})
			.then(function (response) {
				return response.json();
				// redirect to the home page
			})
			.then(function (data) {
				console.log(data);
				window.location.href = "/notes";
			})
			.catch(function (error) {
				console.log(error);
			});
	}
});

// populate the notes on the page
function populateNotes() {
	//get the notes from the server
	let allNotes = getNotes();
	//get the notes container
	let notesContainer = document.getElementById("notes");
	//loop through the notes
	for (let i = 0; i < allNotes.length; i++) {
		//create the note
		let note = document.createElement("div");
		note.classList.add("note");
		//create the title
		let title = document.createElement("h2");
		title.classList.add("title");
		title.innerHTML = allNotes[i].title;
		//create the description
		let description = document.createElement("p");
		description.classList.add("description");
		description.innerHTML = allNotes[i].description;
		//create the tags
		let tags = document.createElement("p");
		tags.classList.add("tags");
		tags.innerHTML = allNotes[i].tags;
		//create the image
		let image = document.createElement("img");
		image.classList.add("image");
		image.src = allNotes[i].image;
		//create the link
		let link = document.createElement("a");
		link.classList.add("link");
		link.href = allNotes[i].link;
		link.innerHTML = "Read More";
		//append the elements to the note
		note.appendChild(title);
		note.appendChild(description);
		note.appendChild(tags);
		note.appendChild(image);
		note.appendChild(link);
		//append the note to the notes container
		notesContainer.appendChild(note);
	}
}
