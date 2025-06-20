const form = document.getElementById('shortenForm');
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const longUrl = document.getElementById('longUrl').value;

    const response = await fetch('https://url-shortener-2-0be1.onrender.com/shorten', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ long_url: longUrl }),
    });

    const data = await response.json();
    document.getElementById('result').innerHTML = `
        Short URL: <a href="${data.short_url}" target="_blank">${data.short_url}</a>
    `;
});
