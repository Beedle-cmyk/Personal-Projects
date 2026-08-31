let danger = "Danger!";
let merge =  `Whats Up, ${danger}`;
console.log(merge);
console.log(typeof merge);

let num = 5;
let decimalNumber = 0.6

console.log();

if(false) {
    console.log('hi man')
} else {
    console.log("hi there bud")
}

const person = {
    name: "John",
    age: 25,
}

console.log(person.name)

const date = new Date()
console.log(date)

for(let i = 0; i <= 10; i++){
    console.log(i)
} 

function sayHi(name) {
    console.log(`Hi, ${name}`);
}

sayHi('Joe');

// Arrow Functions JS

const square = (number) => {
    return number * number
}

console.log(square(5))