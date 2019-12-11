class Animator {

	constructor() {
		this.animationStack = [];
		this.animationTime = 500;
	}

	addToAnimationStack(animation, args){
		this.animationStack.push([animation, args]);
	}

	animate(animator){
		if(this.animationStack.length == 0){
			clearTimeout(animator);
			return;
		}

		let animation = this.animationStack.shift();
		let anim = animation[0];
		let args = animation[1];

		let self = this;
		animator = setTimeout(function() {
			anim(args);
			self.animate(animator);
		}, this.animationTime);
	}
}
