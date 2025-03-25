<a id="readme-top"></a>

<h1 align="center">Renegade Platinum Wiki</h1>

<div align="center">

[![Contributors][contributors-shield]][contributors-url] [![Forks][forks-shield]][forks-url] [![Stargazers][stars-shield]][stars-url] [![Issues][issues-shield]][issues-url] [![MIT License][license-shield]][license-url] [![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<div>
  <p align="center">
    Renegade Platinum Wiki Generator is an automated documentation generator designed specifically for the Renegade Platinum ROM hack of Pokémon Platinum. This project processes raw game data—such as Pokémon stats, movesets, wild encounters, trainer rosters, item changes, and more—and transforms it into a clean, searchable MkDocs-powered wiki.
    <br />
    <br />
    The tool helps ROM hack developers and players alike by providing a browsable reference of in-game changes in a structured, modern web format. It combines custom Python scripts and Markdown generation to output a professional-grade wiki that can be deployed or shared with the community.
    <br />
    <br />
    <a href="https://zhenga8533.github.io/renegade-platinum-wiki">View Demo</a>
    &middot;
    <a href="https://github.com/zhenga8533/renegade-platinum-wiki/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/zhenga8533/renegade-platinum-wiki/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Renegade Platinum Wiki is a fully browsable, static documentation site built to showcase all gameplay changes introduced in the Pokémon ROM hack Renegade Platinum, created by Drayano. These hacks reimagine Pokémon Platinum with a significantly rebalanced difficulty, competitive viability, and expanded content.

The purpose of this project is to provide an organized and easily searchable reference for players, content creators, and developers who want to understand and navigate the massive overhaul these hacks provide.

📦 What This Tool Does

The Renegade Platinum Wiki Generator reads and parses structured raw data files (provided as .txt files in the src/files/ directory), processes them via custom Python scripts (in the src/ directory), and generates organized, readable Markdown documentation into the docs/ directory. The final site is rendered using MkDocs, producing a clean, static site that can be hosted anywhere or viewed locally.

📚 What’s Included in the Wiki

- Pokémon Database: Each Pokémon has a dedicated page outlining its revised stats, learnsets, evolution info, and ability changes.
- Trainer Rosters: Pages for important NPCs and major battles show updated lineups, levels, and strategies.
- Wild Encounters: Area-by-area breakdowns of encounter tables in caves, routes, cities, and special locations.
- Item & Trade Info: Highlights modified held items, new trade options, and balance tweaks.
- Code Reference: Includes documented Action Replay codes tailored for Renegade Platinum.

🎯 Why This Exists

ROM hacks like Renegade Platinum are massive in scope, and documenting every game mechanic manually is a monumental task. This project removes that overhead by automating the entire documentation pipeline. It’s especially useful for:

- Players who want to explore and understand game mechanics in detail
- Content creators and streamers seeking accurate reference material
- Developers creating or modifying similar hacks
- QA testers verifying balance and encounter changes

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Python][Python.org]][Python-url]
- [![MkDocs][MkDocs]][MkDocs-url]
- [![MkDocs Material][MkDocsMaterial]][MkDocsMaterial-url]
- [![Markdown][Markdown]][Markdown-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy of the Renegade Platinum Wiki Generator up and running, follow these steps to install dependencies and generate your own documentation site.

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or higher
- pip (Python package installer)
- Git (optional, for cloning)

### Installation

1. Clone the repository

```bash
git clone https://github.com/zhenga8533/renegade-platinum-wiki.git
cd renegade-platinum-wiki
```

2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install required Python packages

```bash
pip install -r requirements.txt
```

4. Create a .env file based on .env.example if environment variables are used.

5. Generate the Wiki Content

```bash
bash src/main.sh
```

6. View the Wiki Locally

```bash
mkdocs serve
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/zhenga8533/renegade-platinum-wiki/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=zhenga8533/renegade-platinum-wiki" alt="contrib.rocks image" />
</a>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Allen Zheng - zhenga8533@gmail.com

Project Link: [https://github.com/zhenga8533/renegade-platinum-wiki](https://github.com/zhenga8533/renegade-platinum-wiki)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

Special thanks to the following resources and individuals who made this project possible:

- [PokéAPI](https://pokeapi.co) – for data reference and Pokémon-related resources
- [Drayano](https://x.com/drayano60) – creator of the Renegade Platinum ROM hacks that inspired this project
- [Best README Template](https://github.com/othneildrew/Best-README-Template/tree/main) – for providing the foundation for this README format

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/zhenga8533/renegade-platinum-wiki.svg?style=for-the-badge
[contributors-url]: https://github.com/zhenga8533/renegade-platinum-wiki/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/zhenga8533/renegade-platinum-wiki.svg?style=for-the-badge
[forks-url]: https://github.com/zhenga8533/renegade-platinum-wiki/network/members
[stars-shield]: https://img.shields.io/github/stars/zhenga8533/renegade-platinum-wiki.svg?style=for-the-badge
[stars-url]: https://github.com/zhenga8533/renegade-platinum-wiki/stargazers
[issues-shield]: https://img.shields.io/github/issues/zhenga8533/renegade-platinum-wiki.svg?style=for-the-badge
[issues-url]: https://github.com/zhenga8533/renegade-platinum-wiki/issues
[license-shield]: https://img.shields.io/github/license/zhenga8533/renegade-platinum-wiki.svg?style=for-the-badge
[license-url]: https://github.com/zhenga8533/renegade-platinum-wiki/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/zhenga8533

<!-- Built With -->

[Python.org]: https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[MkDocs]: https://img.shields.io/badge/MkDocs-000000?style=for-the-badge&logo=mkdocs&logoColor=white
[MkDocs-url]: https://www.mkdocs.org/
[MkDocsMaterial]: https://img.shields.io/badge/MkDocs--Material-2396F3?style=for-the-badge&logo=materialdesign&logoColor=white
[MkDocsMaterial-url]: https://squidfunk.github.io/mkdocs-material/
[Markdown]: https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white
[Markdown-url]: https://www.markdownguide.org/
