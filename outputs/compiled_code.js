let context = document.getElementById('canvas').getContext('2d');
let g = new Galapagos(context, 0, 10, 50, 50);
let t = new Turtle(context, g, 10, 10, 0);

t.moveStraight(40);
t.turnLeft(90);
t.moveStraight(50);
t.turnRight(20);
t.moveStraight(200);
t.turnLeft(30);
t.moveStraight(200);
t.takeOff();
t.moveStraight(20);
t.landing();
t.turnRight(80);
t.moveStraight(40);
