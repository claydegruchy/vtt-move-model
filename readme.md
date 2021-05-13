# goal
moving a picture or shape on tabletop moves a character in a game

# method
1. capture image (perhaps from video)
	- SmartCam app, this allows a stream in a variety of formats and outputs to http://<IP>:8080/live.jpg, which can be queried endlessly
2. process to recognise shape
3. get shape position
4. find relative position compared to virtual tabletop
5. move token in game to position in video 
