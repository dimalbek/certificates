# certificates
1. Create venv and activate
```
python3 -m venv venv
source venv/bin/activate
```
2. install dependencies

```
pip install -r requirements.txt
```

3. if sqllite is not installed, install it
```
brew install sqlite
```

4. run the app 
```
uvicorn main:app --reload
```
