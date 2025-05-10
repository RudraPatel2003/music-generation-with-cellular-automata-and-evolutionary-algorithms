# cs420-project

This project uses **cellular automata** and **genetic algorithms** to generate music. It includes a web app that generates five cellular automata, each with its own rule set and genome. The user selects between two automata they prefer, and a new generation is created using mutation and crossover.

## Setup and Installation

### Miniconda (Recommended)

While not strictly required, it is highly recommended to use a Python virtual environment to manage dependencies. These instructions use **Miniconda**, but other virtual environment managers should also work. You can find installation instructions for Miniconda on their [official website](https://www.anaconda.com/docs/getting-started/miniconda/main).

> **NOTE:** Regardless of which virtual environment manager you use, ensure that you're using **Python 3.11**.

Create and activate the environment:

```bash
conda create -n cs420-project python=3.11
conda activate cs420-project
```

### SoundFont File

To generate `.mid` files, a SoundFont (`.sf2`) file is required. Any `.sf2` file should work, but this project uses one created by **Arachno**. To use it, copy your `.sf2` file to the following directory:

```bash
/music_player/<your_sound_font_file.sf2>
```

### FluidSynth

To convert `.mid` files into `.mp3`, you'll need **FluidSynth**, a software synthesizer that uses SoundFont files. Installation varies by operating system, but on most Linux distributions, use:

```bash
sudo apt-get install fluidsynth
```

### FFmpeg

FFmpeg is required for generating graphs and visualizations in the web app.

```bash
sudo apt-get install ffmpeg
```

## Usage

To run the web app, use:

```bash
python app.py
```

The app will randomly generate five cellular automata. The user selects between two automata based on the sound they prefer. A new generation is then formed by clicking the **Submit** button. To reset the gene pool and generate five new automata, click the **Reset** button.

All cellular automata operations occur at the file system level for code simplicity and web app stability.

All generated `.json`, `.mp3`, and `.png` files for each generation can be found in the `static/uploads` directory.

## Hall of Fame

To save a cellular automaton to the Hall of Fame, copy its `.json`, `.mp3`, and `.png` files from the `static/uploads` directory to the `static/hall_of_fame` directory.

## Contact

For setup or usage issues, contact:

- Trishu Patel: <tpatel25@vols.utk.edu>

- Rudra Patel: <rpate112@vols.utk.edu>
