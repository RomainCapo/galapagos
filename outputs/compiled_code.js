let context = document.getElementById('canvas').getContext('2d');

let g = new Galapagos(context, 10, 10, 400, 200);
let t = new Turtle(context, g, 10, 10, 0);
t.moveStraight(40);
t.turnRight(90);
t.moveStraight(50);
