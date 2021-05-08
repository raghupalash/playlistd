document.addEventListener('DOMContentLoaded', () => {
    form = document.querySelector('#recently-add-form');
    playlists = document.querySelector('.user-playlists');
    playlistButton = document.querySelector('#reveal-playlists');
    newPlaylistButton = document.querySelector('#new-playlist');
    inputGroup = document.querySelector('#create-playlist-input');

    // For 'Add to playlist' Button
    playlistButton.style.display = 'block';
    playlists.style.display = 'none';

    playlistButton.onclick = () => {
        // Hide button
        playlistButton.style.display = 'none';

        // Show user playlists
        playlists.style.display = 'block';
    }

    // For 'New Playlist' button
    newPlaylistButton.style.display = 'block';
    inputGroup.style.display = 'none';

    newPlaylistButton.onclick = () => {
        // Hide button
        newPlaylistButton.style.display = 'none';

        // Show user playlists
        inputGroup.style.display = 'block';
    }

    document.querySelectorAll('.playlist-add-btn').forEach(btn => {
        btn.onclick = e => {
            // Give value to hidden playlist-name input
            document.querySelector('#playlist-id').value = e.target.id;

            // Submit Form
            form.submit();
        }
    })
})
