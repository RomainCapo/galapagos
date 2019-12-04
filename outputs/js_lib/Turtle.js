class Turtle
{

  constructor(context, galapagos, startPosX, startPosY, startAngle)
  {
    this.context = context;
    this.galapagos = galapagos;
    this.posX = this.galapagos.posX + startPosX;
    this.posY = this.galapagos.posY + startPosY;
    this.angle = this._degToRad(-startAngle);
    this.isGrounded = true;
  }
  
  _loadImage()

  _drawTurtlePos()
  {
	let drawing = new Image();
	drawing.src = "js_lib/turtle.png";
	drawing.onload = () => {
	context.drawImage(drawing,this.posX-15,this.posY-15);
	}
  }

  turnRight(angle)
  {
    this.angle += this._degToRad(-angle);
	this._drawTurtlePos();
  }

  turnLeft(angle)
  {
    this.angle -= this._degToRad(-angle);
	this._drawTurtlePos();
  }

  takeOff()
  {
    this.isGrounded = false;
  }

  landing()
  {
    this.isGrounded = true;
  }

  moveStraight(distance)
  {
    this.context.strokeStyle = '#000000';
    this.context.beginPath();
    this.context.moveTo(this.posX, this.posY);
    this.posX += distance * Math.cos(this.angle);
    this.posY += distance * Math.sin(this.angle);
    this.context.lineTo(this.posX, this.posY)
    if(this.isGrounded)
    {
    this.context.stroke()
    }
	this._drawTurtlePos();
  }

  moveBack(distance)
  {
    this.moveStraight(-distance);
	this._drawTurtlePos();
  }

  getPosX()
  {
    return this.posX - this.galapagos.posX;
  }

  getPosY()
  {
    return this.posY - this.galapagos.posY;
  }

  _degToRad(deg)
  {
    return deg * (Math.PI/180);
  }

 }
