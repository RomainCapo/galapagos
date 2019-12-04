let context = document.getElementById('canvas').getContext('2d');
let g = new Galapagos(context, 0, 10, 50, 50);
let t = new Turtle(context, g, 10, 10, 0);
t.moveStraight(10);
t.moveBack(10);
t.turnLeft(10);
t.turnRight(10);
t.takeOff();
t.landing();
