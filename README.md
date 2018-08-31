# demosys-py-simlife

*WORK IN PROGRESS*

A python port the demo "Sim Life" using demosys-py.

![screenshot1](https://camo.githubusercontent.com/32ce052715e574ae4e6fc60384b5070cbc9aaa27/68747470733a2f2f6f626a656374732e7a657474612e696f3a383434332f76312f415554485f30366532646265613565383234363230623230623437303139373332333237372f636f6e7472617a2e6e6f2d7374617469632f6766782f70726f64756374696f6e732f53696d4c696665332e706e67) ![screenshot2](https://camo.githubusercontent.com/653387f2f7f144b29b6fb9c891a17482b089e02d/68747470733a2f2f6f626a656374732e7a657474612e696f3a383434332f76312f415554485f30366532646265613565383234363230623230623437303139373332333237372f636f6e7472617a2e6e6f2d7374617469632f6766782f70726f64756374696f6e732f53696d4c696665322e706e67)

## Project Structure

### Local Dev

```
python3 -m virtualenv env
./env/bin/activate
pip install -r requirements.txt
```

### Resources

* Resources specific to an effect is located inside each respective effect package
* Global or shared resources are located in ``simlife/resources``. The path to this directory is added in settings

### Effect Packages

* underwater
