from setuptools import setup, find_packages
from pathlib import Path
# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name='eternalblue',
    version='1.3.1',
    description='A diarization package',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/rhaymisonbetini/eternalblue',
    author='Rhaymison Betini',
    author_email='rhaymisoncristian@gmail.com',
    license='Apache 2.0',
    packages=['eternalblue'],
    include_package_data=True,
    package_data={
        'eternalblue': ['public/**/*'],
    },
    install_requires=[
        'transformers~=4.38.2',
        'pyannote.audio',
        'torch~=2.1.2',
        'torchaudio~=2.1.2',
        'torchvision',
        'pydub~=0.25.1',
        'accelerate',
        'noisereduce~=3.0.2',
        'librosa~=0.10.1',
        'python-dotenv',
        'soundfile~=0.12.1',
        'bitsandbytes',
        'insanely-fast-whisper',
        'optimum',
        'openai'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',
)