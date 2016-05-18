'use strict'

/*
 * Implement your "nextMove" and "isValid" functions.
 * You are free to add more functions or remove any function.
 * If you are not clear about the rules, click the "Game Rules" button on the player bar.
 */

const compute = (board) => {
	// Implement Your AI Here
	return "UP";
}

process.stdin.on('data', data => {
	// parse stdin to lines
	const lines = data.toString().split('\n');

	// game board
	const board = lines.slice(0, 4).map(l => l.split(' ').map(s => +s));

	// compute my move and print it to stdout
	console.log(compute(board));
});
