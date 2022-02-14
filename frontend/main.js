const { time } = require("console");

// Join strings
let word_1 = "Hello";
let word_2 = " Hi";
let join_1 = "hello" + word_2;
let join_2 = word_1.concat(word_2);
console.log(join_1, join_2);

// Length of the string
password = "Hello123";
if (password.length > 8) {
  console.log("Good");
} else {
  console.log("Bad");
}

// Search for a string inside another string (Casesensitive)
let email = "kitto@gmail.com";
let validEmail = email.includes("@gmail.com");
if (validEmail) {
  console.log("Valid Email");
} else {
  console.log("Notvalid Email");
}

// String equality comparison
let password1 = "hello1";
let password2 = "hello2";
let validPassword = password1 === password2;
if (validPassword) {
  console.log("Valid Password");
} else {
  console.log("Notvalid Password");
}

// Sort a collection of strings (In-place)
let arr = ["AB", "BC", "AA"];
arr.sort();
console.log(arr);

// Split strings by a pattern
let csv = "one,two,three,";
console.log(csv.split(","));
let sentence = "one two three";
let split = sentence.split(" ");
console.log("word count" + split.length);

// Number (not a number - NaN)
let str = "18";
console.log(Number(str), Math.PI, Math.pow(2, 3), Math.max(100, 30, 2, 1000));

// Boolean
if (validPassword || validEmail) console.log("True");
let valid = validPassword !== validEmail;
console.log(valid);

// Object
let object = { title: "JS", written: "Priya Kheersagar", content: 10 };
console.log(object.title, object);
object.content = object.content + 2;
console.log(object.content);
// Nested Array
let object1 = { title: "CSS", written: "Priya Kheersagar", content: 10 };
let object2 = { css: object1, js: Object };
console.log(object2);

// Array
split[0] = "english";
console.log(split[0], split);
let arr1 = [object1, object2];
console.log(arr1);

// Function
let fun = (name, dept) => {
  let math = Math.floor(Math.random() * 100);
  console.log(name + " " + dept + " " + math);
};
fun("Priya", "CSE");

let fun1 = () => {
  let result = [];
  result.push(str);
  return { status: "Failed", result: result };
};
if (fun1().status == "Failed") console.log("Success");

let sumOfSquaresSingleLine = (x, y) => Math.pow(x, 2) + Math.pow(y, 2);

let sumOfSquaresMultiLine = (x, y) => {
  return Math.pow(x, 2) + Math.pow(y, 2);
};

// Passing a function as an argument
// setTimeout - call when time expires(once)
// setInterval - repeatedly call with fixed time delay

let timeOut = setTimeout(fun, 5 * 1000);
console.log(timeOut);
clearTimeout(timeOut);
let timeInterval = setInterval(fun, 3 * 1000);
console.log(timeInterval);
clearInterval(timeInterval);

// Collections

arr.forEach((value) => console.log(value));
let for_array = (value) => console.log(value);
arr.forEach(for_array);
console.log(arr.join("\n"));
arr.forEach((value, index) => {
  console.log(value + " " + (index + 1));
});

let arr2 = [
  [0, 1, 2, 3],
  [4, 5, 6],
  [7, 8, 9],
];
let sum = 0;
arr2.forEach((item, i) => item.forEach((item, index) => (sum += i)));
console.log(sum);

// Transforming the array
let reverse = (item) => item.split("").reverse().join("");
console.log(reverse("Hello, Hi"));
let rev_array = reverse("Hello, Hi");
console.log(rev_array);

console.log(
  [1, 2, 3, 4, 5].map((item) => {
    let x = item * item;
    let y = item + item;
    return (2 * x) / y;
  }).length
);
// answer is 5

// Filter an array based on some criteria
let filter = [
  { title: "one", status: "good" },
  { title: "two", status: "good" },
  { title: "two", status: "good" },
];

let filter_arr = filter.filter((item) => item.title == "two");
console.log(filter_arr);

console.log(
  [-1, 1, 3, 4, -5].filter((item) => {
    return item > 0;
  }).length
);
// answer : 3

// Use the index of the array value with filter
let weekdays = 7;
const WED = 3;
let arr_week = [1, 2, 3, 5, 6, 23, 45, 23, 89, 67, 90, 45, 67, 12, 89];
let week = (n) => n % weekdays;
let result_week = arr_week.filter((item, index) => week(index) == WED);
console.log(result_week);
