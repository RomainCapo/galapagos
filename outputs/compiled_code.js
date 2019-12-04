let context = document.getElementById('canvas').getContext('2d');
let g = new Galapagos(context, 0, 10, 50, 50);
let t = new Turtle(context, g, 10, 10, 0);

let animator = new Animator()

animator.addToAnimationStack(t.moveStraight.bind(t), 40)
animator.addToAnimationStack(t.turnLeft.bind(t), 90)
animator.addToAnimationStack(t.moveStraight.bind(t), 50)
animator.addToAnimationStack(t.turnRight.bind(t), 20)
animator.addToAnimationStack(t.moveStraight.bind(t), 200)
animator.addToAnimationStack(t.turnLeft.bind(t), 30)
animator.addToAnimationStack(t.moveStraight.bind(t), 20)
animator.addToAnimationStack(t.takeOff.bind(t), null)
animator.addToAnimationStack(t.moveStraight.bind(t), 20)
animator.addToAnimationStack(t.landing.bind(t), null)
animator.addToAnimationStack(t.turnRight.bind(t), 80)
animator.addToAnimationStack(t.moveStraight.bind(t), 40)

animator.animate(null)
