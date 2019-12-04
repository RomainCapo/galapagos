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
    this._drawTurtlePos();
  }

  _drawTurtlePos()
  {
    this.context.fillRect(this.posX, this.posY, 3 , 3);
  }

  turnRight(angle)
  {
    this.angle += this._degToRad(-angle);
  }

  turnLeft(angle)
  {
    this.angle -= this._degToRad(-angle);
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
  }

  moveBack(distance)
  {
    this.moveStraight(-distance);
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
