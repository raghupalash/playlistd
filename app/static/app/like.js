document.addEventListener('DOMContentLoaded', function() {
    let posts = document.querySelectorAll('.like').forEach(function(like) {
        const playlistID = like.dataset.id

        let likesOnPost;
        // Writes the number of likes on the page
        fetch(`/like/${playlistID}`)
        .then(response => response.json())
        .then(data => {
            // like button based on if user has already liked the post or not

            let i = like.querySelector('i')
            if (data.likedByUser === true) {
                i.classList.add("fas");
                i.classList.remove("far");
            } else {
                i.classList.add("far");
                i.classList.remove("fas");
            }

            likesOnPost = data.likes;
            like.querySelector('span').innerHTML = likesOnPost;
        });

        // Triggered when like is clicked
        like.addEventListener('click', () => {

            let i = like.querySelector('i')
            if (i.classList.contains('far')) {
                i.classList.add("fas");
                i.classList.remove("far");

                // Increment
                action = "liked";

                // Updating the frontend
                likesOnPost++;
                like.querySelector('span').innerHTML = likesOnPost;
            } else {
            
                i.classList.add("far");
                i.classList.remove("fas")

                // Decrement
                action = "unliked";

                // Updating the frontend
                likesOnPost--;
                like.querySelector('span').innerHTML = likesOnPost;
            }

            const url = new Request(
                `http://127.0.0.1:8000/like/${playlistID}`,
                {headers: {'X-CSRFToken': csrftoken}}
            );
            // Update the likes count (increment)
            fetch(url, {
                method: 'PUT',
                body: JSON.stringify({
                    action: action
                }),
                mode: 'same-origin'
            });
        });
    });
});