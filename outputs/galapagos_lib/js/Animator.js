class Animator {

	constructor() {
		this.animationTime = 500;
		this.animationDelay = 500;
	}

	animate(anim, args){
		setTimeout(() => {
			anim(args)
		}, this.animationTime);
		this.animationTime+=this.animationDelay;
	}

	animationsDone(){
		setTimeout(() => {
			document.getElementById("execution_info").innerHTML = "Execution finished !";
			document.getElementById("loader").style.display = "None";
		}, this.animationTime);
	}
}
