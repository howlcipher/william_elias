# William Elias - Resume Website

A professional, modern, and highly performant resume website built with HTML, CSS, and Vanilla JavaScript. Deployed via GitHub Pages.

## Features
- **Config-Driven**: Easily update your experience, skills, and contact info via a single `config.js` file. No need to touch HTML!
- **Dark/Light Mode**: User preference is stored in LocalStorage.
- **Colorblind / High-Contrast Mode**: Built-in accessibility theme.
- **Mobile Responsive**: Custom hamburger menu and flexible layout.
- **Print/PDF Download**: Embedded download link for the PDF version.

## How to Update Your Information

You do not need to understand HTML to update this site. All your information is stored in the `config.js` file.

1. Open `config.js` in any text editor.
2. Edit the text inside the quotes.
3. Save the file.
4. Push your changes to the `main` branch to automatically deploy to GitHub Pages.

### Adding a New Job
Find the `experience` array in `config.js` and add a new object to the top of the list:

```javascript
{
    date: "March 2026 - Present",
    title: "Senior Security Engineer",
    company: "New Company Inc.",
    location: "Remote",
    achievements: [
        "First bullet point goes here.",
        "Second bullet point goes here."
    ]
}
```

## Local Development
Since this is a static site, you can simply double-click `index.html` to view it locally in your browser. 

## Deployment
Changes pushed to the `main` branch are automatically deployed via GitHub Pages.
