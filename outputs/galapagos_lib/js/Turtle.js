class Turtle
{

	constructor(context, galapagos, startPosX, startPosY, startAngle){
		this.context = context;
		this.galapagos = galapagos;
		this.posX = startPosX;
		this.posY = startPosY;
		this.angle = this._degToRad(startAngle);
		this.isGrounded = true;
		this.turtleImage = document.getElementById("turtle_image");
		this.nbDrawnTurtle = 0;
	}

  _deleteTurtle(){
    if(this.nbDrawnTurtle != 0)
    {
      this.context.globalCompositeOperation ="xor"
      this.context.drawImage(this.turtleImage, this.posX - 15, this.posY - 15);
      this.context.globalCompositeOperation ="source-over"
    }
  }

	_drawTurtlePos(){
    this.context.drawImage(this.turtleImage, this.posX - 15, this.posY - 15);
    this.nbDrawnTurtle++;
	}

	turnRight(angle){
		this._deleteTurtle();
		this.angle -= this._degToRad(-angle);
		this._drawTurtlePos();
	}

	turnLeft(angle){
		this._deleteTurtle();
		this.angle += this._degToRad(-angle);
		this._drawTurtlePos();
	}

	takeOff(){
		this.isGrounded = false;
	}

	landing(){
		this.isGrounded = true;
	}

	moveStraight(distance){
    this._deleteTurtle();
		this.context.strokeStyle = '#000000';
		this.context.beginPath();
		this.context.moveTo(this.posX, this.posY);
		this.posX += distance * Math.cos(this.angle);
		this.posY += distance * Math.sin(this.angle);
		this.context.lineTo(this.posX, this.posY)
		if(this.isGrounded){
			this.context.stroke()
		}
		this._drawTurtlePos();
	}

	moveBack(distance){
    	this._deleteTurtle();
		this.moveStraight(-distance);
		this._drawTurtlePos();
	}

	getPosX(){
		return this.posX;
	}

	getPosY(){
		return this.posY;
	}

	_degToRad(deg){
		return deg * (Math.PI/180);
	}

}
