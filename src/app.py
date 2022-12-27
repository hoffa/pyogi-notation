import tempfile
import zipfile
from pathlib import Path

import streamlit as st

from parse import parse
from render import render

st.set_page_config(page_title="Pyogi Converter", page_icon=":notes:")
st.title("Pyogi Converter")

st.markdown("Convert scores into the [Pyogi notation](https://pyogi.org).")

f = st.file_uploader("File", help="File must be in MusicXML format.", type=["mxl"])
if f:
    # TODO: Can't get music21 to accept zipped MusicXML bytes as input
    with tempfile.TemporaryDirectory() as dir:
        with zipfile.ZipFile(f) as zip:
            zip.extractall(dir)
            # Assumes only a single top-level XML file
            paths = list(Path(dir).glob("*.xml"))
            if len(paths) == 1:
                filename = paths[0]
                b = render(parse(filename), f.name, f.name)[0]
                st.subheader("Result")
                st.image(b)
                st.download_button("Download", b, "result.svg")

st.caption("Source code available [here](https://github.com/hoffa/pyogi-notation).")
