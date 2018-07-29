from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='ml_board',
      version='0.0.1',
      description="A machine learning dashboard that displays hyperparameter settings alongside visualizations, and logs the scientist's thoughts throughout the training process",
      long_description = long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/bbli/ml_board',
      author='Benson Li',
      scripts=['bin/ml_board'],
      author_email='bensonbinbinli@gmail.com',
      license='MIT',
      packages=['ml_board'],
      classifiers=(
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          )
      )
