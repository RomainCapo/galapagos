class Galapagos
	{
	constructor(context, posX, posY, width, height){
		this.context = context;
		this.posX = posX;
		this.posY = posY;
		this.width = width;
		this.height = height;

		this.drawGalapagos();
	}

	drawGalapagos(){
		this.context.beginPath();
		this.context.strokeStyle = '#16a085';
		this.context.rect(this.posX, this.posY, this.width, this.height);
		this.context.stroke();
	}
}
