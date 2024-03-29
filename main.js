(function(scope){
'use strict';

function F(arity, fun, wrapper) {
  wrapper.a = arity;
  wrapper.f = fun;
  return wrapper;
}

function F2(fun) {
  return F(2, fun, function(a) { return function(b) { return fun(a,b); }; })
}
function F3(fun) {
  return F(3, fun, function(a) {
    return function(b) { return function(c) { return fun(a, b, c); }; };
  });
}
function F4(fun) {
  return F(4, fun, function(a) { return function(b) { return function(c) {
    return function(d) { return fun(a, b, c, d); }; }; };
  });
}
function F5(fun) {
  return F(5, fun, function(a) { return function(b) { return function(c) {
    return function(d) { return function(e) { return fun(a, b, c, d, e); }; }; }; };
  });
}
function F6(fun) {
  return F(6, fun, function(a) { return function(b) { return function(c) {
    return function(d) { return function(e) { return function(f) {
    return fun(a, b, c, d, e, f); }; }; }; }; };
  });
}
function F7(fun) {
  return F(7, fun, function(a) { return function(b) { return function(c) {
    return function(d) { return function(e) { return function(f) {
    return function(g) { return fun(a, b, c, d, e, f, g); }; }; }; }; }; };
  });
}
function F8(fun) {
  return F(8, fun, function(a) { return function(b) { return function(c) {
    return function(d) { return function(e) { return function(f) {
    return function(g) { return function(h) {
    return fun(a, b, c, d, e, f, g, h); }; }; }; }; }; }; };
  });
}
function F9(fun) {
  return F(9, fun, function(a) { return function(b) { return function(c) {
    return function(d) { return function(e) { return function(f) {
    return function(g) { return function(h) { return function(i) {
    return fun(a, b, c, d, e, f, g, h, i); }; }; }; }; }; }; }; };
  });
}

function A2(fun, a, b) {
  return fun.a === 2 ? fun.f(a, b) : fun(a)(b);
}
function A3(fun, a, b, c) {
  return fun.a === 3 ? fun.f(a, b, c) : fun(a)(b)(c);
}
function A4(fun, a, b, c, d) {
  return fun.a === 4 ? fun.f(a, b, c, d) : fun(a)(b)(c)(d);
}
function A5(fun, a, b, c, d, e) {
  return fun.a === 5 ? fun.f(a, b, c, d, e) : fun(a)(b)(c)(d)(e);
}
function A6(fun, a, b, c, d, e, f) {
  return fun.a === 6 ? fun.f(a, b, c, d, e, f) : fun(a)(b)(c)(d)(e)(f);
}
function A7(fun, a, b, c, d, e, f, g) {
  return fun.a === 7 ? fun.f(a, b, c, d, e, f, g) : fun(a)(b)(c)(d)(e)(f)(g);
}
function A8(fun, a, b, c, d, e, f, g, h) {
  return fun.a === 8 ? fun.f(a, b, c, d, e, f, g, h) : fun(a)(b)(c)(d)(e)(f)(g)(h);
}
function A9(fun, a, b, c, d, e, f, g, h, i) {
  return fun.a === 9 ? fun.f(a, b, c, d, e, f, g, h, i) : fun(a)(b)(c)(d)(e)(f)(g)(h)(i);
}

console.warn('Compiled in DEV mode. Follow the advice at https://elm-lang.org/0.19.1/optimize for better performance and smaller assets.');


// EQUALITY

function _Utils_eq(x, y)
{
	for (
		var pair, stack = [], isEqual = _Utils_eqHelp(x, y, 0, stack);
		isEqual && (pair = stack.pop());
		isEqual = _Utils_eqHelp(pair.a, pair.b, 0, stack)
		)
	{}

	return isEqual;
}

function _Utils_eqHelp(x, y, depth, stack)
{
	if (x === y)
	{
		return true;
	}

	if (typeof x !== 'object' || x === null || y === null)
	{
		typeof x === 'function' && _Debug_crash(5);
		return false;
	}

	if (depth > 100)
	{
		stack.push(_Utils_Tuple2(x,y));
		return true;
	}

	/**/
	if (x.$ === 'Set_elm_builtin')
	{
		x = $elm$core$Set$toList(x);
		y = $elm$core$Set$toList(y);
	}
	if (x.$ === 'RBNode_elm_builtin' || x.$ === 'RBEmpty_elm_builtin')
	{
		x = $elm$core$Dict$toList(x);
		y = $elm$core$Dict$toList(y);
	}
	//*/

	/**_UNUSED/
	if (x.$ < 0)
	{
		x = $elm$core$Dict$toList(x);
		y = $elm$core$Dict$toList(y);
	}
	//*/

	for (var key in x)
	{
		if (!_Utils_eqHelp(x[key], y[key], depth + 1, stack))
		{
			return false;
		}
	}
	return true;
}

var _Utils_equal = F2(_Utils_eq);
var _Utils_notEqual = F2(function(a, b) { return !_Utils_eq(a,b); });



// COMPARISONS

// Code in Generate/JavaScript.hs, Basics.js, and List.js depends on
// the particular integer values assigned to LT, EQ, and GT.

function _Utils_cmp(x, y, ord)
{
	if (typeof x !== 'object')
	{
		return x === y ? /*EQ*/ 0 : x < y ? /*LT*/ -1 : /*GT*/ 1;
	}

	/**/
	if (x instanceof String)
	{
		var a = x.valueOf();
		var b = y.valueOf();
		return a === b ? 0 : a < b ? -1 : 1;
	}
	//*/

	/**_UNUSED/
	if (typeof x.$ === 'undefined')
	//*/
	/**/
	if (x.$[0] === '#')
	//*/
	{
		return (ord = _Utils_cmp(x.a, y.a))
			? ord
			: (ord = _Utils_cmp(x.b, y.b))
				? ord
				: _Utils_cmp(x.c, y.c);
	}

	// traverse conses until end of a list or a mismatch
	for (; x.b && y.b && !(ord = _Utils_cmp(x.a, y.a)); x = x.b, y = y.b) {} // WHILE_CONSES
	return ord || (x.b ? /*GT*/ 1 : y.b ? /*LT*/ -1 : /*EQ*/ 0);
}

var _Utils_lt = F2(function(a, b) { return _Utils_cmp(a, b) < 0; });
var _Utils_le = F2(function(a, b) { return _Utils_cmp(a, b) < 1; });
var _Utils_gt = F2(function(a, b) { return _Utils_cmp(a, b) > 0; });
var _Utils_ge = F2(function(a, b) { return _Utils_cmp(a, b) >= 0; });

var _Utils_compare = F2(function(x, y)
{
	var n = _Utils_cmp(x, y);
	return n < 0 ? $elm$core$Basics$LT : n ? $elm$core$Basics$GT : $elm$core$Basics$EQ;
});


// COMMON VALUES

var _Utils_Tuple0_UNUSED = 0;
var _Utils_Tuple0 = { $: '#0' };

function _Utils_Tuple2_UNUSED(a, b) { return { a: a, b: b }; }
function _Utils_Tuple2(a, b) { return { $: '#2', a: a, b: b }; }

function _Utils_Tuple3_UNUSED(a, b, c) { return { a: a, b: b, c: c }; }
function _Utils_Tuple3(a, b, c) { return { $: '#3', a: a, b: b, c: c }; }

function _Utils_chr_UNUSED(c) { return c; }
function _Utils_chr(c) { return new String(c); }


// RECORDS

function _Utils_update(oldRecord, updatedFields)
{
	var newRecord = {};

	for (var key in oldRecord)
	{
		newRecord[key] = oldRecord[key];
	}

	for (var key in updatedFields)
	{
		newRecord[key] = updatedFields[key];
	}

	return newRecord;
}


// APPEND

var _Utils_append = F2(_Utils_ap);

function _Utils_ap(xs, ys)
{
	// append Strings
	if (typeof xs === 'string')
	{
		return xs + ys;
	}

	// append Lists
	if (!xs.b)
	{
		return ys;
	}
	var root = _List_Cons(xs.a, ys);
	xs = xs.b
	for (var curr = root; xs.b; xs = xs.b) // WHILE_CONS
	{
		curr = curr.b = _List_Cons(xs.a, ys);
	}
	return root;
}



var _List_Nil_UNUSED = { $: 0 };
var _List_Nil = { $: '[]' };

function _List_Cons_UNUSED(hd, tl) { return { $: 1, a: hd, b: tl }; }
function _List_Cons(hd, tl) { return { $: '::', a: hd, b: tl }; }


var _List_cons = F2(_List_Cons);

function _List_fromArray(arr)
{
	var out = _List_Nil;
	for (var i = arr.length; i--; )
	{
		out = _List_Cons(arr[i], out);
	}
	return out;
}

function _List_toArray(xs)
{
	for (var out = []; xs.b; xs = xs.b) // WHILE_CONS
	{
		out.push(xs.a);
	}
	return out;
}

var _List_map2 = F3(function(f, xs, ys)
{
	for (var arr = []; xs.b && ys.b; xs = xs.b, ys = ys.b) // WHILE_CONSES
	{
		arr.push(A2(f, xs.a, ys.a));
	}
	return _List_fromArray(arr);
});

var _List_map3 = F4(function(f, xs, ys, zs)
{
	for (var arr = []; xs.b && ys.b && zs.b; xs = xs.b, ys = ys.b, zs = zs.b) // WHILE_CONSES
	{
		arr.push(A3(f, xs.a, ys.a, zs.a));
	}
	return _List_fromArray(arr);
});

var _List_map4 = F5(function(f, ws, xs, ys, zs)
{
	for (var arr = []; ws.b && xs.b && ys.b && zs.b; ws = ws.b, xs = xs.b, ys = ys.b, zs = zs.b) // WHILE_CONSES
	{
		arr.push(A4(f, ws.a, xs.a, ys.a, zs.a));
	}
	return _List_fromArray(arr);
});

var _List_map5 = F6(function(f, vs, ws, xs, ys, zs)
{
	for (var arr = []; vs.b && ws.b && xs.b && ys.b && zs.b; vs = vs.b, ws = ws.b, xs = xs.b, ys = ys.b, zs = zs.b) // WHILE_CONSES
	{
		arr.push(A5(f, vs.a, ws.a, xs.a, ys.a, zs.a));
	}
	return _List_fromArray(arr);
});

var _List_sortBy = F2(function(f, xs)
{
	return _List_fromArray(_List_toArray(xs).sort(function(a, b) {
		return _Utils_cmp(f(a), f(b));
	}));
});

var _List_sortWith = F2(function(f, xs)
{
	return _List_fromArray(_List_toArray(xs).sort(function(a, b) {
		var ord = A2(f, a, b);
		return ord === $elm$core$Basics$EQ ? 0 : ord === $elm$core$Basics$LT ? -1 : 1;
	}));
});



var _JsArray_empty = [];

function _JsArray_singleton(value)
{
    return [value];
}

function _JsArray_length(array)
{
    return array.length;
}

var _JsArray_initialize = F3(function(size, offset, func)
{
    var result = new Array(size);

    for (var i = 0; i < size; i++)
    {
        result[i] = func(offset + i);
    }

    return result;
});

var _JsArray_initializeFromList = F2(function (max, ls)
{
    var result = new Array(max);

    for (var i = 0; i < max && ls.b; i++)
    {
        result[i] = ls.a;
        ls = ls.b;
    }

    result.length = i;
    return _Utils_Tuple2(result, ls);
});

var _JsArray_unsafeGet = F2(function(index, array)
{
    return array[index];
});

var _JsArray_unsafeSet = F3(function(index, value, array)
{
    var length = array.length;
    var result = new Array(length);

    for (var i = 0; i < length; i++)
    {
        result[i] = array[i];
    }

    result[index] = value;
    return result;
});

var _JsArray_push = F2(function(value, array)
{
    var length = array.length;
    var result = new Array(length + 1);

    for (var i = 0; i < length; i++)
    {
        result[i] = array[i];
    }

    result[length] = value;
    return result;
});

var _JsArray_foldl = F3(function(func, acc, array)
{
    var length = array.length;

    for (var i = 0; i < length; i++)
    {
        acc = A2(func, array[i], acc);
    }

    return acc;
});

var _JsArray_foldr = F3(function(func, acc, array)
{
    for (var i = array.length - 1; i >= 0; i--)
    {
        acc = A2(func, array[i], acc);
    }

    return acc;
});

var _JsArray_map = F2(function(func, array)
{
    var length = array.length;
    var result = new Array(length);

    for (var i = 0; i < length; i++)
    {
        result[i] = func(array[i]);
    }

    return result;
});

var _JsArray_indexedMap = F3(function(func, offset, array)
{
    var length = array.length;
    var result = new Array(length);

    for (var i = 0; i < length; i++)
    {
        result[i] = A2(func, offset + i, array[i]);
    }

    return result;
});

var _JsArray_slice = F3(function(from, to, array)
{
    return array.slice(from, to);
});

var _JsArray_appendN = F3(function(n, dest, source)
{
    var destLen = dest.length;
    var itemsToCopy = n - destLen;

    if (itemsToCopy > source.length)
    {
        itemsToCopy = source.length;
    }

    var size = destLen + itemsToCopy;
    var result = new Array(size);

    for (var i = 0; i < destLen; i++)
    {
        result[i] = dest[i];
    }

    for (var i = 0; i < itemsToCopy; i++)
    {
        result[i + destLen] = source[i];
    }

    return result;
});



// LOG

var _Debug_log_UNUSED = F2(function(tag, value)
{
	return value;
});

var _Debug_log = F2(function(tag, value)
{
	console.log(tag + ': ' + _Debug_toString(value));
	return value;
});


// TODOS

function _Debug_todo(moduleName, region)
{
	return function(message) {
		_Debug_crash(8, moduleName, region, message);
	};
}

function _Debug_todoCase(moduleName, region, value)
{
	return function(message) {
		_Debug_crash(9, moduleName, region, value, message);
	};
}


// TO STRING

function _Debug_toString_UNUSED(value)
{
	return '<internals>';
}

function _Debug_toString(value)
{
	return _Debug_toAnsiString(false, value);
}

function _Debug_toAnsiString(ansi, value)
{
	if (typeof value === 'function')
	{
		return _Debug_internalColor(ansi, '<function>');
	}

	if (typeof value === 'boolean')
	{
		return _Debug_ctorColor(ansi, value ? 'True' : 'False');
	}

	if (typeof value === 'number')
	{
		return _Debug_numberColor(ansi, value + '');
	}

	if (value instanceof String)
	{
		return _Debug_charColor(ansi, "'" + _Debug_addSlashes(value, true) + "'");
	}

	if (typeof value === 'string')
	{
		return _Debug_stringColor(ansi, '"' + _Debug_addSlashes(value, false) + '"');
	}

	if (typeof value === 'object' && '$' in value)
	{
		var tag = value.$;

		if (typeof tag === 'number')
		{
			return _Debug_internalColor(ansi, '<internals>');
		}

		if (tag[0] === '#')
		{
			var output = [];
			for (var k in value)
			{
				if (k === '$') continue;
				output.push(_Debug_toAnsiString(ansi, value[k]));
			}
			return '(' + output.join(',') + ')';
		}

		if (tag === 'Set_elm_builtin')
		{
			return _Debug_ctorColor(ansi, 'Set')
				+ _Debug_fadeColor(ansi, '.fromList') + ' '
				+ _Debug_toAnsiString(ansi, $elm$core$Set$toList(value));
		}

		if (tag === 'RBNode_elm_builtin' || tag === 'RBEmpty_elm_builtin')
		{
			return _Debug_ctorColor(ansi, 'Dict')
				+ _Debug_fadeColor(ansi, '.fromList') + ' '
				+ _Debug_toAnsiString(ansi, $elm$core$Dict$toList(value));
		}

		if (tag === 'Array_elm_builtin')
		{
			return _Debug_ctorColor(ansi, 'Array')
				+ _Debug_fadeColor(ansi, '.fromList') + ' '
				+ _Debug_toAnsiString(ansi, $elm$core$Array$toList(value));
		}

		if (tag === '::' || tag === '[]')
		{
			var output = '[';

			value.b && (output += _Debug_toAnsiString(ansi, value.a), value = value.b)

			for (; value.b; value = value.b) // WHILE_CONS
			{
				output += ',' + _Debug_toAnsiString(ansi, value.a);
			}
			return output + ']';
		}

		var output = '';
		for (var i in value)
		{
			if (i === '$') continue;
			var str = _Debug_toAnsiString(ansi, value[i]);
			var c0 = str[0];
			var parenless = c0 === '{' || c0 === '(' || c0 === '[' || c0 === '<' || c0 === '"' || str.indexOf(' ') < 0;
			output += ' ' + (parenless ? str : '(' + str + ')');
		}
		return _Debug_ctorColor(ansi, tag) + output;
	}

	if (typeof DataView === 'function' && value instanceof DataView)
	{
		return _Debug_stringColor(ansi, '<' + value.byteLength + ' bytes>');
	}

	if (typeof File !== 'undefined' && value instanceof File)
	{
		return _Debug_internalColor(ansi, '<' + value.name + '>');
	}

	if (typeof value === 'object')
	{
		var output = [];
		for (var key in value)
		{
			var field = key[0] === '_' ? key.slice(1) : key;
			output.push(_Debug_fadeColor(ansi, field) + ' = ' + _Debug_toAnsiString(ansi, value[key]));
		}
		if (output.length === 0)
		{
			return '{}';
		}
		return '{ ' + output.join(', ') + ' }';
	}

	return _Debug_internalColor(ansi, '<internals>');
}

function _Debug_addSlashes(str, isChar)
{
	var s = str
		.replace(/\\/g, '\\\\')
		.replace(/\n/g, '\\n')
		.replace(/\t/g, '\\t')
		.replace(/\r/g, '\\r')
		.replace(/\v/g, '\\v')
		.replace(/\0/g, '\\0');

	if (isChar)
	{
		return s.replace(/\'/g, '\\\'');
	}
	else
	{
		return s.replace(/\"/g, '\\"');
	}
}

function _Debug_ctorColor(ansi, string)
{
	return ansi ? '\x1b[96m' + string + '\x1b[0m' : string;
}

function _Debug_numberColor(ansi, string)
{
	return ansi ? '\x1b[95m' + string + '\x1b[0m' : string;
}

function _Debug_stringColor(ansi, string)
{
	return ansi ? '\x1b[93m' + string + '\x1b[0m' : string;
}

function _Debug_charColor(ansi, string)
{
	return ansi ? '\x1b[92m' + string + '\x1b[0m' : string;
}

function _Debug_fadeColor(ansi, string)
{
	return ansi ? '\x1b[37m' + string + '\x1b[0m' : string;
}

function _Debug_internalColor(ansi, string)
{
	return ansi ? '\x1b[36m' + string + '\x1b[0m' : string;
}

function _Debug_toHexDigit(n)
{
	return String.fromCharCode(n < 10 ? 48 + n : 55 + n);
}


// CRASH


function _Debug_crash_UNUSED(identifier)
{
	throw new Error('https://github.com/elm/core/blob/1.0.0/hints/' + identifier + '.md');
}


function _Debug_crash(identifier, fact1, fact2, fact3, fact4)
{
	switch(identifier)
	{
		case 0:
			throw new Error('What node should I take over? In JavaScript I need something like:\n\n    Elm.Main.init({\n        node: document.getElementById("elm-node")\n    })\n\nYou need to do this with any Browser.sandbox or Browser.element program.');

		case 1:
			throw new Error('Browser.application programs cannot handle URLs like this:\n\n    ' + document.location.href + '\n\nWhat is the root? The root of your file system? Try looking at this program with `elm reactor` or some other server.');

		case 2:
			var jsonErrorString = fact1;
			throw new Error('Problem with the flags given to your Elm program on initialization.\n\n' + jsonErrorString);

		case 3:
			var portName = fact1;
			throw new Error('There can only be one port named `' + portName + '`, but your program has multiple.');

		case 4:
			var portName = fact1;
			var problem = fact2;
			throw new Error('Trying to send an unexpected type of value through port `' + portName + '`:\n' + problem);

		case 5:
			throw new Error('Trying to use `(==)` on functions.\nThere is no way to know if functions are "the same" in the Elm sense.\nRead more about this at https://package.elm-lang.org/packages/elm/core/latest/Basics#== which describes why it is this way and what the better version will look like.');

		case 6:
			var moduleName = fact1;
			throw new Error('Your page is loading multiple Elm scripts with a module named ' + moduleName + '. Maybe a duplicate script is getting loaded accidentally? If not, rename one of them so I know which is which!');

		case 8:
			var moduleName = fact1;
			var region = fact2;
			var message = fact3;
			throw new Error('TODO in module `' + moduleName + '` ' + _Debug_regionToString(region) + '\n\n' + message);

		case 9:
			var moduleName = fact1;
			var region = fact2;
			var value = fact3;
			var message = fact4;
			throw new Error(
				'TODO in module `' + moduleName + '` from the `case` expression '
				+ _Debug_regionToString(region) + '\n\nIt received the following value:\n\n    '
				+ _Debug_toString(value).replace('\n', '\n    ')
				+ '\n\nBut the branch that handles it says:\n\n    ' + message.replace('\n', '\n    ')
			);

		case 10:
			throw new Error('Bug in https://github.com/elm/virtual-dom/issues');

		case 11:
			throw new Error('Cannot perform mod 0. Division by zero error.');
	}
}

function _Debug_regionToString(region)
{
	if (region.start.line === region.end.line)
	{
		return 'on line ' + region.start.line;
	}
	return 'on lines ' + region.start.line + ' through ' + region.end.line;
}



// MATH

var _Basics_add = F2(function(a, b) { return a + b; });
var _Basics_sub = F2(function(a, b) { return a - b; });
var _Basics_mul = F2(function(a, b) { return a * b; });
var _Basics_fdiv = F2(function(a, b) { return a / b; });
var _Basics_idiv = F2(function(a, b) { return (a / b) | 0; });
var _Basics_pow = F2(Math.pow);

var _Basics_remainderBy = F2(function(b, a) { return a % b; });

// https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/divmodnote-letter.pdf
var _Basics_modBy = F2(function(modulus, x)
{
	var answer = x % modulus;
	return modulus === 0
		? _Debug_crash(11)
		:
	((answer > 0 && modulus < 0) || (answer < 0 && modulus > 0))
		? answer + modulus
		: answer;
});


// TRIGONOMETRY

var _Basics_pi = Math.PI;
var _Basics_e = Math.E;
var _Basics_cos = Math.cos;
var _Basics_sin = Math.sin;
var _Basics_tan = Math.tan;
var _Basics_acos = Math.acos;
var _Basics_asin = Math.asin;
var _Basics_atan = Math.atan;
var _Basics_atan2 = F2(Math.atan2);


// MORE MATH

function _Basics_toFloat(x) { return x; }
function _Basics_truncate(n) { return n | 0; }
function _Basics_isInfinite(n) { return n === Infinity || n === -Infinity; }

var _Basics_ceiling = Math.ceil;
var _Basics_floor = Math.floor;
var _Basics_round = Math.round;
var _Basics_sqrt = Math.sqrt;
var _Basics_log = Math.log;
var _Basics_isNaN = isNaN;


// BOOLEANS

function _Basics_not(bool) { return !bool; }
var _Basics_and = F2(function(a, b) { return a && b; });
var _Basics_or  = F2(function(a, b) { return a || b; });
var _Basics_xor = F2(function(a, b) { return a !== b; });



var _String_cons = F2(function(chr, str)
{
	return chr + str;
});

function _String_uncons(string)
{
	var word = string.charCodeAt(0);
	return !isNaN(word)
		? $elm$core$Maybe$Just(
			0xD800 <= word && word <= 0xDBFF
				? _Utils_Tuple2(_Utils_chr(string[0] + string[1]), string.slice(2))
				: _Utils_Tuple2(_Utils_chr(string[0]), string.slice(1))
		)
		: $elm$core$Maybe$Nothing;
}

var _String_append = F2(function(a, b)
{
	return a + b;
});

function _String_length(str)
{
	return str.length;
}

var _String_map = F2(function(func, string)
{
	var len = string.length;
	var array = new Array(len);
	var i = 0;
	while (i < len)
	{
		var word = string.charCodeAt(i);
		if (0xD800 <= word && word <= 0xDBFF)
		{
			array[i] = func(_Utils_chr(string[i] + string[i+1]));
			i += 2;
			continue;
		}
		array[i] = func(_Utils_chr(string[i]));
		i++;
	}
	return array.join('');
});

var _String_filter = F2(function(isGood, str)
{
	var arr = [];
	var len = str.length;
	var i = 0;
	while (i < len)
	{
		var char = str[i];
		var word = str.charCodeAt(i);
		i++;
		if (0xD800 <= word && word <= 0xDBFF)
		{
			char += str[i];
			i++;
		}

		if (isGood(_Utils_chr(char)))
		{
			arr.push(char);
		}
	}
	return arr.join('');
});

function _String_reverse(str)
{
	var len = str.length;
	var arr = new Array(len);
	var i = 0;
	while (i < len)
	{
		var word = str.charCodeAt(i);
		if (0xD800 <= word && word <= 0xDBFF)
		{
			arr[len - i] = str[i + 1];
			i++;
			arr[len - i] = str[i - 1];
			i++;
		}
		else
		{
			arr[len - i] = str[i];
			i++;
		}
	}
	return arr.join('');
}

var _String_foldl = F3(function(func, state, string)
{
	var len = string.length;
	var i = 0;
	while (i < len)
	{
		var char = string[i];
		var word = string.charCodeAt(i);
		i++;
		if (0xD800 <= word && word <= 0xDBFF)
		{
			char += string[i];
			i++;
		}
		state = A2(func, _Utils_chr(char), state);
	}
	return state;
});

var _String_foldr = F3(function(func, state, string)
{
	var i = string.length;
	while (i--)
	{
		var char = string[i];
		var word = string.charCodeAt(i);
		if (0xDC00 <= word && word <= 0xDFFF)
		{
			i--;
			char = string[i] + char;
		}
		state = A2(func, _Utils_chr(char), state);
	}
	return state;
});

var _String_split = F2(function(sep, str)
{
	return str.split(sep);
});

var _String_join = F2(function(sep, strs)
{
	return strs.join(sep);
});

var _String_slice = F3(function(start, end, str) {
	return str.slice(start, end);
});

function _String_trim(str)
{
	return str.trim();
}

function _String_trimLeft(str)
{
	return str.replace(/^\s+/, '');
}

function _String_trimRight(str)
{
	return str.replace(/\s+$/, '');
}

function _String_words(str)
{
	return _List_fromArray(str.trim().split(/\s+/g));
}

function _String_lines(str)
{
	return _List_fromArray(str.split(/\r\n|\r|\n/g));
}

function _String_toUpper(str)
{
	return str.toUpperCase();
}

function _String_toLower(str)
{
	return str.toLowerCase();
}

var _String_any = F2(function(isGood, string)
{
	var i = string.length;
	while (i--)
	{
		var char = string[i];
		var word = string.charCodeAt(i);
		if (0xDC00 <= word && word <= 0xDFFF)
		{
			i--;
			char = string[i] + char;
		}
		if (isGood(_Utils_chr(char)))
		{
			return true;
		}
	}
	return false;
});

var _String_all = F2(function(isGood, string)
{
	var i = string.length;
	while (i--)
	{
		var char = string[i];
		var word = string.charCodeAt(i);
		if (0xDC00 <= word && word <= 0xDFFF)
		{
			i--;
			char = string[i] + char;
		}
		if (!isGood(_Utils_chr(char)))
		{
			return false;
		}
	}
	return true;
});

var _String_contains = F2(function(sub, str)
{
	return str.indexOf(sub) > -1;
});

var _String_startsWith = F2(function(sub, str)
{
	return str.indexOf(sub) === 0;
});

var _String_endsWith = F2(function(sub, str)
{
	return str.length >= sub.length &&
		str.lastIndexOf(sub) === str.length - sub.length;
});

var _String_indexes = F2(function(sub, str)
{
	var subLen = sub.length;

	if (subLen < 1)
	{
		return _List_Nil;
	}

	var i = 0;
	var is = [];

	while ((i = str.indexOf(sub, i)) > -1)
	{
		is.push(i);
		i = i + subLen;
	}

	return _List_fromArray(is);
});


// TO STRING

function _String_fromNumber(number)
{
	return number + '';
}


// INT CONVERSIONS

function _String_toInt(str)
{
	var total = 0;
	var code0 = str.charCodeAt(0);
	var start = code0 == 0x2B /* + */ || code0 == 0x2D /* - */ ? 1 : 0;

	for (var i = start; i < str.length; ++i)
	{
		var code = str.charCodeAt(i);
		if (code < 0x30 || 0x39 < code)
		{
			return $elm$core$Maybe$Nothing;
		}
		total = 10 * total + code - 0x30;
	}

	return i == start
		? $elm$core$Maybe$Nothing
		: $elm$core$Maybe$Just(code0 == 0x2D ? -total : total);
}


// FLOAT CONVERSIONS

function _String_toFloat(s)
{
	// check if it is a hex, octal, or binary number
	if (s.length === 0 || /[\sxbo]/.test(s))
	{
		return $elm$core$Maybe$Nothing;
	}
	var n = +s;
	// faster isNaN check
	return n === n ? $elm$core$Maybe$Just(n) : $elm$core$Maybe$Nothing;
}

function _String_fromList(chars)
{
	return _List_toArray(chars).join('');
}




function _Char_toCode(char)
{
	var code = char.charCodeAt(0);
	if (0xD800 <= code && code <= 0xDBFF)
	{
		return (code - 0xD800) * 0x400 + char.charCodeAt(1) - 0xDC00 + 0x10000
	}
	return code;
}

function _Char_fromCode(code)
{
	return _Utils_chr(
		(code < 0 || 0x10FFFF < code)
			? '\uFFFD'
			:
		(code <= 0xFFFF)
			? String.fromCharCode(code)
			:
		(code -= 0x10000,
			String.fromCharCode(Math.floor(code / 0x400) + 0xD800, code % 0x400 + 0xDC00)
		)
	);
}

function _Char_toUpper(char)
{
	return _Utils_chr(char.toUpperCase());
}

function _Char_toLower(char)
{
	return _Utils_chr(char.toLowerCase());
}

function _Char_toLocaleUpper(char)
{
	return _Utils_chr(char.toLocaleUpperCase());
}

function _Char_toLocaleLower(char)
{
	return _Utils_chr(char.toLocaleLowerCase());
}



/**/
function _Json_errorToString(error)
{
	return $elm$json$Json$Decode$errorToString(error);
}
//*/


// CORE DECODERS

function _Json_succeed(msg)
{
	return {
		$: 0,
		a: msg
	};
}

function _Json_fail(msg)
{
	return {
		$: 1,
		a: msg
	};
}

function _Json_decodePrim(decoder)
{
	return { $: 2, b: decoder };
}

var _Json_decodeInt = _Json_decodePrim(function(value) {
	return (typeof value !== 'number')
		? _Json_expecting('an INT', value)
		:
	(-2147483647 < value && value < 2147483647 && (value | 0) === value)
		? $elm$core$Result$Ok(value)
		:
	(isFinite(value) && !(value % 1))
		? $elm$core$Result$Ok(value)
		: _Json_expecting('an INT', value);
});

var _Json_decodeBool = _Json_decodePrim(function(value) {
	return (typeof value === 'boolean')
		? $elm$core$Result$Ok(value)
		: _Json_expecting('a BOOL', value);
});

var _Json_decodeFloat = _Json_decodePrim(function(value) {
	return (typeof value === 'number')
		? $elm$core$Result$Ok(value)
		: _Json_expecting('a FLOAT', value);
});

var _Json_decodeValue = _Json_decodePrim(function(value) {
	return $elm$core$Result$Ok(_Json_wrap(value));
});

var _Json_decodeString = _Json_decodePrim(function(value) {
	return (typeof value === 'string')
		? $elm$core$Result$Ok(value)
		: (value instanceof String)
			? $elm$core$Result$Ok(value + '')
			: _Json_expecting('a STRING', value);
});

function _Json_decodeList(decoder) { return { $: 3, b: decoder }; }
function _Json_decodeArray(decoder) { return { $: 4, b: decoder }; }

function _Json_decodeNull(value) { return { $: 5, c: value }; }

var _Json_decodeField = F2(function(field, decoder)
{
	return {
		$: 6,
		d: field,
		b: decoder
	};
});

var _Json_decodeIndex = F2(function(index, decoder)
{
	return {
		$: 7,
		e: index,
		b: decoder
	};
});

function _Json_decodeKeyValuePairs(decoder)
{
	return {
		$: 8,
		b: decoder
	};
}

function _Json_mapMany(f, decoders)
{
	return {
		$: 9,
		f: f,
		g: decoders
	};
}

var _Json_andThen = F2(function(callback, decoder)
{
	return {
		$: 10,
		b: decoder,
		h: callback
	};
});

function _Json_oneOf(decoders)
{
	return {
		$: 11,
		g: decoders
	};
}


// DECODING OBJECTS

var _Json_map1 = F2(function(f, d1)
{
	return _Json_mapMany(f, [d1]);
});

var _Json_map2 = F3(function(f, d1, d2)
{
	return _Json_mapMany(f, [d1, d2]);
});

var _Json_map3 = F4(function(f, d1, d2, d3)
{
	return _Json_mapMany(f, [d1, d2, d3]);
});

var _Json_map4 = F5(function(f, d1, d2, d3, d4)
{
	return _Json_mapMany(f, [d1, d2, d3, d4]);
});

var _Json_map5 = F6(function(f, d1, d2, d3, d4, d5)
{
	return _Json_mapMany(f, [d1, d2, d3, d4, d5]);
});

var _Json_map6 = F7(function(f, d1, d2, d3, d4, d5, d6)
{
	return _Json_mapMany(f, [d1, d2, d3, d4, d5, d6]);
});

var _Json_map7 = F8(function(f, d1, d2, d3, d4, d5, d6, d7)
{
	return _Json_mapMany(f, [d1, d2, d3, d4, d5, d6, d7]);
});

var _Json_map8 = F9(function(f, d1, d2, d3, d4, d5, d6, d7, d8)
{
	return _Json_mapMany(f, [d1, d2, d3, d4, d5, d6, d7, d8]);
});


// DECODE

var _Json_runOnString = F2(function(decoder, string)
{
	try
	{
		var value = JSON.parse(string);
		return _Json_runHelp(decoder, value);
	}
	catch (e)
	{
		return $elm$core$Result$Err(A2($elm$json$Json$Decode$Failure, 'This is not valid JSON! ' + e.message, _Json_wrap(string)));
	}
});

var _Json_run = F2(function(decoder, value)
{
	return _Json_runHelp(decoder, _Json_unwrap(value));
});

function _Json_runHelp(decoder, value)
{
	switch (decoder.$)
	{
		case 2:
			return decoder.b(value);

		case 5:
			return (value === null)
				? $elm$core$Result$Ok(decoder.c)
				: _Json_expecting('null', value);

		case 3:
			if (!_Json_isArray(value))
			{
				return _Json_expecting('a LIST', value);
			}
			return _Json_runArrayDecoder(decoder.b, value, _List_fromArray);

		case 4:
			if (!_Json_isArray(value))
			{
				return _Json_expecting('an ARRAY', value);
			}
			return _Json_runArrayDecoder(decoder.b, value, _Json_toElmArray);

		case 6:
			var field = decoder.d;
			if (typeof value !== 'object' || value === null || !(field in value))
			{
				return _Json_expecting('an OBJECT with a field named `' + field + '`', value);
			}
			var result = _Json_runHelp(decoder.b, value[field]);
			return ($elm$core$Result$isOk(result)) ? result : $elm$core$Result$Err(A2($elm$json$Json$Decode$Field, field, result.a));

		case 7:
			var index = decoder.e;
			if (!_Json_isArray(value))
			{
				return _Json_expecting('an ARRAY', value);
			}
			if (index >= value.length)
			{
				return _Json_expecting('a LONGER array. Need index ' + index + ' but only see ' + value.length + ' entries', value);
			}
			var result = _Json_runHelp(decoder.b, value[index]);
			return ($elm$core$Result$isOk(result)) ? result : $elm$core$Result$Err(A2($elm$json$Json$Decode$Index, index, result.a));

		case 8:
			if (typeof value !== 'object' || value === null || _Json_isArray(value))
			{
				return _Json_expecting('an OBJECT', value);
			}

			var keyValuePairs = _List_Nil;
			// TODO test perf of Object.keys and switch when support is good enough
			for (var key in value)
			{
				if (value.hasOwnProperty(key))
				{
					var result = _Json_runHelp(decoder.b, value[key]);
					if (!$elm$core$Result$isOk(result))
					{
						return $elm$core$Result$Err(A2($elm$json$Json$Decode$Field, key, result.a));
					}
					keyValuePairs = _List_Cons(_Utils_Tuple2(key, result.a), keyValuePairs);
				}
			}
			return $elm$core$Result$Ok($elm$core$List$reverse(keyValuePairs));

		case 9:
			var answer = decoder.f;
			var decoders = decoder.g;
			for (var i = 0; i < decoders.length; i++)
			{
				var result = _Json_runHelp(decoders[i], value);
				if (!$elm$core$Result$isOk(result))
				{
					return result;
				}
				answer = answer(result.a);
			}
			return $elm$core$Result$Ok(answer);

		case 10:
			var result = _Json_runHelp(decoder.b, value);
			return (!$elm$core$Result$isOk(result))
				? result
				: _Json_runHelp(decoder.h(result.a), value);

		case 11:
			var errors = _List_Nil;
			for (var temp = decoder.g; temp.b; temp = temp.b) // WHILE_CONS
			{
				var result = _Json_runHelp(temp.a, value);
				if ($elm$core$Result$isOk(result))
				{
					return result;
				}
				errors = _List_Cons(result.a, errors);
			}
			return $elm$core$Result$Err($elm$json$Json$Decode$OneOf($elm$core$List$reverse(errors)));

		case 1:
			return $elm$core$Result$Err(A2($elm$json$Json$Decode$Failure, decoder.a, _Json_wrap(value)));

		case 0:
			return $elm$core$Result$Ok(decoder.a);
	}
}

function _Json_runArrayDecoder(decoder, value, toElmValue)
{
	var len = value.length;
	var array = new Array(len);
	for (var i = 0; i < len; i++)
	{
		var result = _Json_runHelp(decoder, value[i]);
		if (!$elm$core$Result$isOk(result))
		{
			return $elm$core$Result$Err(A2($elm$json$Json$Decode$Index, i, result.a));
		}
		array[i] = result.a;
	}
	return $elm$core$Result$Ok(toElmValue(array));
}

function _Json_isArray(value)
{
	return Array.isArray(value) || (typeof FileList !== 'undefined' && value instanceof FileList);
}

function _Json_toElmArray(array)
{
	return A2($elm$core$Array$initialize, array.length, function(i) { return array[i]; });
}

function _Json_expecting(type, value)
{
	return $elm$core$Result$Err(A2($elm$json$Json$Decode$Failure, 'Expecting ' + type, _Json_wrap(value)));
}


// EQUALITY

function _Json_equality(x, y)
{
	if (x === y)
	{
		return true;
	}

	if (x.$ !== y.$)
	{
		return false;
	}

	switch (x.$)
	{
		case 0:
		case 1:
			return x.a === y.a;

		case 2:
			return x.b === y.b;

		case 5:
			return x.c === y.c;

		case 3:
		case 4:
		case 8:
			return _Json_equality(x.b, y.b);

		case 6:
			return x.d === y.d && _Json_equality(x.b, y.b);

		case 7:
			return x.e === y.e && _Json_equality(x.b, y.b);

		case 9:
			return x.f === y.f && _Json_listEquality(x.g, y.g);

		case 10:
			return x.h === y.h && _Json_equality(x.b, y.b);

		case 11:
			return _Json_listEquality(x.g, y.g);
	}
}

function _Json_listEquality(aDecoders, bDecoders)
{
	var len = aDecoders.length;
	if (len !== bDecoders.length)
	{
		return false;
	}
	for (var i = 0; i < len; i++)
	{
		if (!_Json_equality(aDecoders[i], bDecoders[i]))
		{
			return false;
		}
	}
	return true;
}


// ENCODE

var _Json_encode = F2(function(indentLevel, value)
{
	return JSON.stringify(_Json_unwrap(value), null, indentLevel) + '';
});

function _Json_wrap(value) { return { $: 0, a: value }; }
function _Json_unwrap(value) { return value.a; }

function _Json_wrap_UNUSED(value) { return value; }
function _Json_unwrap_UNUSED(value) { return value; }

function _Json_emptyArray() { return []; }
function _Json_emptyObject() { return {}; }

var _Json_addField = F3(function(key, value, object)
{
	object[key] = _Json_unwrap(value);
	return object;
});

function _Json_addEntry(func)
{
	return F2(function(entry, array)
	{
		array.push(_Json_unwrap(func(entry)));
		return array;
	});
}

var _Json_encodeNull = _Json_wrap(null);



// TASKS

function _Scheduler_succeed(value)
{
	return {
		$: 0,
		a: value
	};
}

function _Scheduler_fail(error)
{
	return {
		$: 1,
		a: error
	};
}

function _Scheduler_binding(callback)
{
	return {
		$: 2,
		b: callback,
		c: null
	};
}

var _Scheduler_andThen = F2(function(callback, task)
{
	return {
		$: 3,
		b: callback,
		d: task
	};
});

var _Scheduler_onError = F2(function(callback, task)
{
	return {
		$: 4,
		b: callback,
		d: task
	};
});

function _Scheduler_receive(callback)
{
	return {
		$: 5,
		b: callback
	};
}


// PROCESSES

var _Scheduler_guid = 0;

function _Scheduler_rawSpawn(task)
{
	var proc = {
		$: 0,
		e: _Scheduler_guid++,
		f: task,
		g: null,
		h: []
	};

	_Scheduler_enqueue(proc);

	return proc;
}

function _Scheduler_spawn(task)
{
	return _Scheduler_binding(function(callback) {
		callback(_Scheduler_succeed(_Scheduler_rawSpawn(task)));
	});
}

function _Scheduler_rawSend(proc, msg)
{
	proc.h.push(msg);
	_Scheduler_enqueue(proc);
}

var _Scheduler_send = F2(function(proc, msg)
{
	return _Scheduler_binding(function(callback) {
		_Scheduler_rawSend(proc, msg);
		callback(_Scheduler_succeed(_Utils_Tuple0));
	});
});

function _Scheduler_kill(proc)
{
	return _Scheduler_binding(function(callback) {
		var task = proc.f;
		if (task.$ === 2 && task.c)
		{
			task.c();
		}

		proc.f = null;

		callback(_Scheduler_succeed(_Utils_Tuple0));
	});
}


/* STEP PROCESSES

type alias Process =
  { $ : tag
  , id : unique_id
  , root : Task
  , stack : null | { $: SUCCEED | FAIL, a: callback, b: stack }
  , mailbox : [msg]
  }

*/


var _Scheduler_working = false;
var _Scheduler_queue = [];


function _Scheduler_enqueue(proc)
{
	_Scheduler_queue.push(proc);
	if (_Scheduler_working)
	{
		return;
	}
	_Scheduler_working = true;
	while (proc = _Scheduler_queue.shift())
	{
		_Scheduler_step(proc);
	}
	_Scheduler_working = false;
}


function _Scheduler_step(proc)
{
	while (proc.f)
	{
		var rootTag = proc.f.$;
		if (rootTag === 0 || rootTag === 1)
		{
			while (proc.g && proc.g.$ !== rootTag)
			{
				proc.g = proc.g.i;
			}
			if (!proc.g)
			{
				return;
			}
			proc.f = proc.g.b(proc.f.a);
			proc.g = proc.g.i;
		}
		else if (rootTag === 2)
		{
			proc.f.c = proc.f.b(function(newRoot) {
				proc.f = newRoot;
				_Scheduler_enqueue(proc);
			});
			return;
		}
		else if (rootTag === 5)
		{
			if (proc.h.length === 0)
			{
				return;
			}
			proc.f = proc.f.b(proc.h.shift());
		}
		else // if (rootTag === 3 || rootTag === 4)
		{
			proc.g = {
				$: rootTag === 3 ? 0 : 1,
				b: proc.f.b,
				i: proc.g
			};
			proc.f = proc.f.d;
		}
	}
}



function _Process_sleep(time)
{
	return _Scheduler_binding(function(callback) {
		var id = setTimeout(function() {
			callback(_Scheduler_succeed(_Utils_Tuple0));
		}, time);

		return function() { clearTimeout(id); };
	});
}




// PROGRAMS


var _Platform_worker = F4(function(impl, flagDecoder, debugMetadata, args)
{
	return _Platform_initialize(
		flagDecoder,
		args,
		impl.init,
		impl.update,
		impl.subscriptions,
		function() { return function() {} }
	);
});



// INITIALIZE A PROGRAM


function _Platform_initialize(flagDecoder, args, init, update, subscriptions, stepperBuilder)
{
	var result = A2(_Json_run, flagDecoder, _Json_wrap(args ? args['flags'] : undefined));
	$elm$core$Result$isOk(result) || _Debug_crash(2 /**/, _Json_errorToString(result.a) /**/);
	var managers = {};
	var initPair = init(result.a);
	var model = initPair.a;
	var stepper = stepperBuilder(sendToApp, model);
	var ports = _Platform_setupEffects(managers, sendToApp);

	function sendToApp(msg, viewMetadata)
	{
		var pair = A2(update, msg, model);
		stepper(model = pair.a, viewMetadata);
		_Platform_enqueueEffects(managers, pair.b, subscriptions(model));
	}

	_Platform_enqueueEffects(managers, initPair.b, subscriptions(model));

	return ports ? { ports: ports } : {};
}



// TRACK PRELOADS
//
// This is used by code in elm/browser and elm/http
// to register any HTTP requests that are triggered by init.
//


var _Platform_preload;


function _Platform_registerPreload(url)
{
	_Platform_preload.add(url);
}



// EFFECT MANAGERS


var _Platform_effectManagers = {};


function _Platform_setupEffects(managers, sendToApp)
{
	var ports;

	// setup all necessary effect managers
	for (var key in _Platform_effectManagers)
	{
		var manager = _Platform_effectManagers[key];

		if (manager.a)
		{
			ports = ports || {};
			ports[key] = manager.a(key, sendToApp);
		}

		managers[key] = _Platform_instantiateManager(manager, sendToApp);
	}

	return ports;
}


function _Platform_createManager(init, onEffects, onSelfMsg, cmdMap, subMap)
{
	return {
		b: init,
		c: onEffects,
		d: onSelfMsg,
		e: cmdMap,
		f: subMap
	};
}


function _Platform_instantiateManager(info, sendToApp)
{
	var router = {
		g: sendToApp,
		h: undefined
	};

	var onEffects = info.c;
	var onSelfMsg = info.d;
	var cmdMap = info.e;
	var subMap = info.f;

	function loop(state)
	{
		return A2(_Scheduler_andThen, loop, _Scheduler_receive(function(msg)
		{
			var value = msg.a;

			if (msg.$ === 0)
			{
				return A3(onSelfMsg, router, value, state);
			}

			return cmdMap && subMap
				? A4(onEffects, router, value.i, value.j, state)
				: A3(onEffects, router, cmdMap ? value.i : value.j, state);
		}));
	}

	return router.h = _Scheduler_rawSpawn(A2(_Scheduler_andThen, loop, info.b));
}



// ROUTING


var _Platform_sendToApp = F2(function(router, msg)
{
	return _Scheduler_binding(function(callback)
	{
		router.g(msg);
		callback(_Scheduler_succeed(_Utils_Tuple0));
	});
});


var _Platform_sendToSelf = F2(function(router, msg)
{
	return A2(_Scheduler_send, router.h, {
		$: 0,
		a: msg
	});
});



// BAGS


function _Platform_leaf(home)
{
	return function(value)
	{
		return {
			$: 1,
			k: home,
			l: value
		};
	};
}


function _Platform_batch(list)
{
	return {
		$: 2,
		m: list
	};
}


var _Platform_map = F2(function(tagger, bag)
{
	return {
		$: 3,
		n: tagger,
		o: bag
	}
});



// PIPE BAGS INTO EFFECT MANAGERS
//
// Effects must be queued!
//
// Say your init contains a synchronous command, like Time.now or Time.here
//
//   - This will produce a batch of effects (FX_1)
//   - The synchronous task triggers the subsequent `update` call
//   - This will produce a batch of effects (FX_2)
//
// If we just start dispatching FX_2, subscriptions from FX_2 can be processed
// before subscriptions from FX_1. No good! Earlier versions of this code had
// this problem, leading to these reports:
//
//   https://github.com/elm/core/issues/980
//   https://github.com/elm/core/pull/981
//   https://github.com/elm/compiler/issues/1776
//
// The queue is necessary to avoid ordering issues for synchronous commands.


// Why use true/false here? Why not just check the length of the queue?
// The goal is to detect "are we currently dispatching effects?" If we
// are, we need to bail and let the ongoing while loop handle things.
//
// Now say the queue has 1 element. When we dequeue the final element,
// the queue will be empty, but we are still actively dispatching effects.
// So you could get queue jumping in a really tricky category of cases.
//
var _Platform_effectsQueue = [];
var _Platform_effectsActive = false;


function _Platform_enqueueEffects(managers, cmdBag, subBag)
{
	_Platform_effectsQueue.push({ p: managers, q: cmdBag, r: subBag });

	if (_Platform_effectsActive) return;

	_Platform_effectsActive = true;
	for (var fx; fx = _Platform_effectsQueue.shift(); )
	{
		_Platform_dispatchEffects(fx.p, fx.q, fx.r);
	}
	_Platform_effectsActive = false;
}


function _Platform_dispatchEffects(managers, cmdBag, subBag)
{
	var effectsDict = {};
	_Platform_gatherEffects(true, cmdBag, effectsDict, null);
	_Platform_gatherEffects(false, subBag, effectsDict, null);

	for (var home in managers)
	{
		_Scheduler_rawSend(managers[home], {
			$: 'fx',
			a: effectsDict[home] || { i: _List_Nil, j: _List_Nil }
		});
	}
}


function _Platform_gatherEffects(isCmd, bag, effectsDict, taggers)
{
	switch (bag.$)
	{
		case 1:
			var home = bag.k;
			var effect = _Platform_toEffect(isCmd, home, taggers, bag.l);
			effectsDict[home] = _Platform_insert(isCmd, effect, effectsDict[home]);
			return;

		case 2:
			for (var list = bag.m; list.b; list = list.b) // WHILE_CONS
			{
				_Platform_gatherEffects(isCmd, list.a, effectsDict, taggers);
			}
			return;

		case 3:
			_Platform_gatherEffects(isCmd, bag.o, effectsDict, {
				s: bag.n,
				t: taggers
			});
			return;
	}
}


function _Platform_toEffect(isCmd, home, taggers, value)
{
	function applyTaggers(x)
	{
		for (var temp = taggers; temp; temp = temp.t)
		{
			x = temp.s(x);
		}
		return x;
	}

	var map = isCmd
		? _Platform_effectManagers[home].e
		: _Platform_effectManagers[home].f;

	return A2(map, applyTaggers, value)
}


function _Platform_insert(isCmd, newEffect, effects)
{
	effects = effects || { i: _List_Nil, j: _List_Nil };

	isCmd
		? (effects.i = _List_Cons(newEffect, effects.i))
		: (effects.j = _List_Cons(newEffect, effects.j));

	return effects;
}



// PORTS


function _Platform_checkPortName(name)
{
	if (_Platform_effectManagers[name])
	{
		_Debug_crash(3, name)
	}
}



// OUTGOING PORTS


function _Platform_outgoingPort(name, converter)
{
	_Platform_checkPortName(name);
	_Platform_effectManagers[name] = {
		e: _Platform_outgoingPortMap,
		u: converter,
		a: _Platform_setupOutgoingPort
	};
	return _Platform_leaf(name);
}


var _Platform_outgoingPortMap = F2(function(tagger, value) { return value; });


function _Platform_setupOutgoingPort(name)
{
	var subs = [];
	var converter = _Platform_effectManagers[name].u;

	// CREATE MANAGER

	var init = _Process_sleep(0);

	_Platform_effectManagers[name].b = init;
	_Platform_effectManagers[name].c = F3(function(router, cmdList, state)
	{
		for ( ; cmdList.b; cmdList = cmdList.b) // WHILE_CONS
		{
			// grab a separate reference to subs in case unsubscribe is called
			var currentSubs = subs;
			var value = _Json_unwrap(converter(cmdList.a));
			for (var i = 0; i < currentSubs.length; i++)
			{
				currentSubs[i](value);
			}
		}
		return init;
	});

	// PUBLIC API

	function subscribe(callback)
	{
		subs.push(callback);
	}

	function unsubscribe(callback)
	{
		// copy subs into a new array in case unsubscribe is called within a
		// subscribed callback
		subs = subs.slice();
		var index = subs.indexOf(callback);
		if (index >= 0)
		{
			subs.splice(index, 1);
		}
	}

	return {
		subscribe: subscribe,
		unsubscribe: unsubscribe
	};
}



// INCOMING PORTS


function _Platform_incomingPort(name, converter)
{
	_Platform_checkPortName(name);
	_Platform_effectManagers[name] = {
		f: _Platform_incomingPortMap,
		u: converter,
		a: _Platform_setupIncomingPort
	};
	return _Platform_leaf(name);
}


var _Platform_incomingPortMap = F2(function(tagger, finalTagger)
{
	return function(value)
	{
		return tagger(finalTagger(value));
	};
});


function _Platform_setupIncomingPort(name, sendToApp)
{
	var subs = _List_Nil;
	var converter = _Platform_effectManagers[name].u;

	// CREATE MANAGER

	var init = _Scheduler_succeed(null);

	_Platform_effectManagers[name].b = init;
	_Platform_effectManagers[name].c = F3(function(router, subList, state)
	{
		subs = subList;
		return init;
	});

	// PUBLIC API

	function send(incomingValue)
	{
		var result = A2(_Json_run, converter, _Json_wrap(incomingValue));

		$elm$core$Result$isOk(result) || _Debug_crash(4, name, result.a);

		var value = result.a;
		for (var temp = subs; temp.b; temp = temp.b) // WHILE_CONS
		{
			sendToApp(temp.a(value));
		}
	}

	return { send: send };
}



// EXPORT ELM MODULES
//
// Have DEBUG and PROD versions so that we can (1) give nicer errors in
// debug mode and (2) not pay for the bits needed for that in prod mode.
//


function _Platform_export_UNUSED(exports)
{
	scope['Elm']
		? _Platform_mergeExportsProd(scope['Elm'], exports)
		: scope['Elm'] = exports;
}


function _Platform_mergeExportsProd(obj, exports)
{
	for (var name in exports)
	{
		(name in obj)
			? (name == 'init')
				? _Debug_crash(6)
				: _Platform_mergeExportsProd(obj[name], exports[name])
			: (obj[name] = exports[name]);
	}
}


function _Platform_export(exports)
{
	scope['Elm']
		? _Platform_mergeExportsDebug('Elm', scope['Elm'], exports)
		: scope['Elm'] = exports;
}


function _Platform_mergeExportsDebug(moduleName, obj, exports)
{
	for (var name in exports)
	{
		(name in obj)
			? (name == 'init')
				? _Debug_crash(6, moduleName)
				: _Platform_mergeExportsDebug(moduleName + '.' + name, obj[name], exports[name])
			: (obj[name] = exports[name]);
	}
}




// HELPERS


var _VirtualDom_divertHrefToApp;

var _VirtualDom_doc = typeof document !== 'undefined' ? document : {};


function _VirtualDom_appendChild(parent, child)
{
	parent.appendChild(child);
}

var _VirtualDom_init = F4(function(virtualNode, flagDecoder, debugMetadata, args)
{
	// NOTE: this function needs _Platform_export available to work

	/**_UNUSED/
	var node = args['node'];
	//*/
	/**/
	var node = args && args['node'] ? args['node'] : _Debug_crash(0);
	//*/

	node.parentNode.replaceChild(
		_VirtualDom_render(virtualNode, function() {}),
		node
	);

	return {};
});



// TEXT


function _VirtualDom_text(string)
{
	return {
		$: 0,
		a: string
	};
}



// NODE


var _VirtualDom_nodeNS = F2(function(namespace, tag)
{
	return F2(function(factList, kidList)
	{
		for (var kids = [], descendantsCount = 0; kidList.b; kidList = kidList.b) // WHILE_CONS
		{
			var kid = kidList.a;
			descendantsCount += (kid.b || 0);
			kids.push(kid);
		}
		descendantsCount += kids.length;

		return {
			$: 1,
			c: tag,
			d: _VirtualDom_organizeFacts(factList),
			e: kids,
			f: namespace,
			b: descendantsCount
		};
	});
});


var _VirtualDom_node = _VirtualDom_nodeNS(undefined);



// KEYED NODE


var _VirtualDom_keyedNodeNS = F2(function(namespace, tag)
{
	return F2(function(factList, kidList)
	{
		for (var kids = [], descendantsCount = 0; kidList.b; kidList = kidList.b) // WHILE_CONS
		{
			var kid = kidList.a;
			descendantsCount += (kid.b.b || 0);
			kids.push(kid);
		}
		descendantsCount += kids.length;

		return {
			$: 2,
			c: tag,
			d: _VirtualDom_organizeFacts(factList),
			e: kids,
			f: namespace,
			b: descendantsCount
		};
	});
});


var _VirtualDom_keyedNode = _VirtualDom_keyedNodeNS(undefined);



// CUSTOM


function _VirtualDom_custom(factList, model, render, diff)
{
	return {
		$: 3,
		d: _VirtualDom_organizeFacts(factList),
		g: model,
		h: render,
		i: diff
	};
}



// MAP


var _VirtualDom_map = F2(function(tagger, node)
{
	return {
		$: 4,
		j: tagger,
		k: node,
		b: 1 + (node.b || 0)
	};
});



// LAZY


function _VirtualDom_thunk(refs, thunk)
{
	return {
		$: 5,
		l: refs,
		m: thunk,
		k: undefined
	};
}

var _VirtualDom_lazy = F2(function(func, a)
{
	return _VirtualDom_thunk([func, a], function() {
		return func(a);
	});
});

var _VirtualDom_lazy2 = F3(function(func, a, b)
{
	return _VirtualDom_thunk([func, a, b], function() {
		return A2(func, a, b);
	});
});

var _VirtualDom_lazy3 = F4(function(func, a, b, c)
{
	return _VirtualDom_thunk([func, a, b, c], function() {
		return A3(func, a, b, c);
	});
});

var _VirtualDom_lazy4 = F5(function(func, a, b, c, d)
{
	return _VirtualDom_thunk([func, a, b, c, d], function() {
		return A4(func, a, b, c, d);
	});
});

var _VirtualDom_lazy5 = F6(function(func, a, b, c, d, e)
{
	return _VirtualDom_thunk([func, a, b, c, d, e], function() {
		return A5(func, a, b, c, d, e);
	});
});

var _VirtualDom_lazy6 = F7(function(func, a, b, c, d, e, f)
{
	return _VirtualDom_thunk([func, a, b, c, d, e, f], function() {
		return A6(func, a, b, c, d, e, f);
	});
});

var _VirtualDom_lazy7 = F8(function(func, a, b, c, d, e, f, g)
{
	return _VirtualDom_thunk([func, a, b, c, d, e, f, g], function() {
		return A7(func, a, b, c, d, e, f, g);
	});
});

var _VirtualDom_lazy8 = F9(function(func, a, b, c, d, e, f, g, h)
{
	return _VirtualDom_thunk([func, a, b, c, d, e, f, g, h], function() {
		return A8(func, a, b, c, d, e, f, g, h);
	});
});



// FACTS


var _VirtualDom_on = F2(function(key, handler)
{
	return {
		$: 'a0',
		n: key,
		o: handler
	};
});
var _VirtualDom_style = F2(function(key, value)
{
	return {
		$: 'a1',
		n: key,
		o: value
	};
});
var _VirtualDom_property = F2(function(key, value)
{
	return {
		$: 'a2',
		n: key,
		o: value
	};
});
var _VirtualDom_attribute = F2(function(key, value)
{
	return {
		$: 'a3',
		n: key,
		o: value
	};
});
var _VirtualDom_attributeNS = F3(function(namespace, key, value)
{
	return {
		$: 'a4',
		n: key,
		o: { f: namespace, o: value }
	};
});



// XSS ATTACK VECTOR CHECKS
//
// For some reason, tabs can appear in href protocols and it still works.
// So '\tjava\tSCRIPT:alert("!!!")' and 'javascript:alert("!!!")' are the same
// in practice. That is why _VirtualDom_RE_js and _VirtualDom_RE_js_html look
// so freaky.
//
// Pulling the regular expressions out to the top level gives a slight speed
// boost in small benchmarks (4-10%) but hoisting values to reduce allocation
// can be unpredictable in large programs where JIT may have a harder time with
// functions are not fully self-contained. The benefit is more that the js and
// js_html ones are so weird that I prefer to see them near each other.


var _VirtualDom_RE_script = /^script$/i;
var _VirtualDom_RE_on_formAction = /^(on|formAction$)/i;
var _VirtualDom_RE_js = /^\s*j\s*a\s*v\s*a\s*s\s*c\s*r\s*i\s*p\s*t\s*:/i;
var _VirtualDom_RE_js_html = /^\s*(j\s*a\s*v\s*a\s*s\s*c\s*r\s*i\s*p\s*t\s*:|d\s*a\s*t\s*a\s*:\s*t\s*e\s*x\s*t\s*\/\s*h\s*t\s*m\s*l\s*(,|;))/i;


function _VirtualDom_noScript(tag)
{
	return _VirtualDom_RE_script.test(tag) ? 'p' : tag;
}

function _VirtualDom_noOnOrFormAction(key)
{
	return _VirtualDom_RE_on_formAction.test(key) ? 'data-' + key : key;
}

function _VirtualDom_noInnerHtmlOrFormAction(key)
{
	return key == 'innerHTML' || key == 'formAction' ? 'data-' + key : key;
}

function _VirtualDom_noJavaScriptUri(value)
{
	return _VirtualDom_RE_js.test(value)
		? /**_UNUSED/''//*//**/'javascript:alert("This is an XSS vector. Please use ports or web components instead.")'//*/
		: value;
}

function _VirtualDom_noJavaScriptOrHtmlUri(value)
{
	return _VirtualDom_RE_js_html.test(value)
		? /**_UNUSED/''//*//**/'javascript:alert("This is an XSS vector. Please use ports or web components instead.")'//*/
		: value;
}

function _VirtualDom_noJavaScriptOrHtmlJson(value)
{
	return (typeof _Json_unwrap(value) === 'string' && _VirtualDom_RE_js_html.test(_Json_unwrap(value)))
		? _Json_wrap(
			/**_UNUSED/''//*//**/'javascript:alert("This is an XSS vector. Please use ports or web components instead.")'//*/
		) : value;
}



// MAP FACTS


var _VirtualDom_mapAttribute = F2(function(func, attr)
{
	return (attr.$ === 'a0')
		? A2(_VirtualDom_on, attr.n, _VirtualDom_mapHandler(func, attr.o))
		: attr;
});

function _VirtualDom_mapHandler(func, handler)
{
	var tag = $elm$virtual_dom$VirtualDom$toHandlerInt(handler);

	// 0 = Normal
	// 1 = MayStopPropagation
	// 2 = MayPreventDefault
	// 3 = Custom

	return {
		$: handler.$,
		a:
			!tag
				? A2($elm$json$Json$Decode$map, func, handler.a)
				:
			A3($elm$json$Json$Decode$map2,
				tag < 3
					? _VirtualDom_mapEventTuple
					: _VirtualDom_mapEventRecord,
				$elm$json$Json$Decode$succeed(func),
				handler.a
			)
	};
}

var _VirtualDom_mapEventTuple = F2(function(func, tuple)
{
	return _Utils_Tuple2(func(tuple.a), tuple.b);
});

var _VirtualDom_mapEventRecord = F2(function(func, record)
{
	return {
		message: func(record.message),
		stopPropagation: record.stopPropagation,
		preventDefault: record.preventDefault
	}
});



// ORGANIZE FACTS


function _VirtualDom_organizeFacts(factList)
{
	for (var facts = {}; factList.b; factList = factList.b) // WHILE_CONS
	{
		var entry = factList.a;

		var tag = entry.$;
		var key = entry.n;
		var value = entry.o;

		if (tag === 'a2')
		{
			(key === 'className')
				? _VirtualDom_addClass(facts, key, _Json_unwrap(value))
				: facts[key] = _Json_unwrap(value);

			continue;
		}

		var subFacts = facts[tag] || (facts[tag] = {});
		(tag === 'a3' && key === 'class')
			? _VirtualDom_addClass(subFacts, key, value)
			: subFacts[key] = value;
	}

	return facts;
}

function _VirtualDom_addClass(object, key, newClass)
{
	var classes = object[key];
	object[key] = classes ? classes + ' ' + newClass : newClass;
}



// RENDER


function _VirtualDom_render(vNode, eventNode)
{
	var tag = vNode.$;

	if (tag === 5)
	{
		return _VirtualDom_render(vNode.k || (vNode.k = vNode.m()), eventNode);
	}

	if (tag === 0)
	{
		return _VirtualDom_doc.createTextNode(vNode.a);
	}

	if (tag === 4)
	{
		var subNode = vNode.k;
		var tagger = vNode.j;

		while (subNode.$ === 4)
		{
			typeof tagger !== 'object'
				? tagger = [tagger, subNode.j]
				: tagger.push(subNode.j);

			subNode = subNode.k;
		}

		var subEventRoot = { j: tagger, p: eventNode };
		var domNode = _VirtualDom_render(subNode, subEventRoot);
		domNode.elm_event_node_ref = subEventRoot;
		return domNode;
	}

	if (tag === 3)
	{
		var domNode = vNode.h(vNode.g);
		_VirtualDom_applyFacts(domNode, eventNode, vNode.d);
		return domNode;
	}

	// at this point `tag` must be 1 or 2

	var domNode = vNode.f
		? _VirtualDom_doc.createElementNS(vNode.f, vNode.c)
		: _VirtualDom_doc.createElement(vNode.c);

	if (_VirtualDom_divertHrefToApp && vNode.c == 'a')
	{
		domNode.addEventListener('click', _VirtualDom_divertHrefToApp(domNode));
	}

	_VirtualDom_applyFacts(domNode, eventNode, vNode.d);

	for (var kids = vNode.e, i = 0; i < kids.length; i++)
	{
		_VirtualDom_appendChild(domNode, _VirtualDom_render(tag === 1 ? kids[i] : kids[i].b, eventNode));
	}

	return domNode;
}



// APPLY FACTS


function _VirtualDom_applyFacts(domNode, eventNode, facts)
{
	for (var key in facts)
	{
		var value = facts[key];

		key === 'a1'
			? _VirtualDom_applyStyles(domNode, value)
			:
		key === 'a0'
			? _VirtualDom_applyEvents(domNode, eventNode, value)
			:
		key === 'a3'
			? _VirtualDom_applyAttrs(domNode, value)
			:
		key === 'a4'
			? _VirtualDom_applyAttrsNS(domNode, value)
			:
		((key !== 'value' && key !== 'checked') || domNode[key] !== value) && (domNode[key] = value);
	}
}



// APPLY STYLES


function _VirtualDom_applyStyles(domNode, styles)
{
	var domNodeStyle = domNode.style;

	for (var key in styles)
	{
		domNodeStyle[key] = styles[key];
	}
}



// APPLY ATTRS


function _VirtualDom_applyAttrs(domNode, attrs)
{
	for (var key in attrs)
	{
		var value = attrs[key];
		typeof value !== 'undefined'
			? domNode.setAttribute(key, value)
			: domNode.removeAttribute(key);
	}
}



// APPLY NAMESPACED ATTRS


function _VirtualDom_applyAttrsNS(domNode, nsAttrs)
{
	for (var key in nsAttrs)
	{
		var pair = nsAttrs[key];
		var namespace = pair.f;
		var value = pair.o;

		typeof value !== 'undefined'
			? domNode.setAttributeNS(namespace, key, value)
			: domNode.removeAttributeNS(namespace, key);
	}
}



// APPLY EVENTS


function _VirtualDom_applyEvents(domNode, eventNode, events)
{
	var allCallbacks = domNode.elmFs || (domNode.elmFs = {});

	for (var key in events)
	{
		var newHandler = events[key];
		var oldCallback = allCallbacks[key];

		if (!newHandler)
		{
			domNode.removeEventListener(key, oldCallback);
			allCallbacks[key] = undefined;
			continue;
		}

		if (oldCallback)
		{
			var oldHandler = oldCallback.q;
			if (oldHandler.$ === newHandler.$)
			{
				oldCallback.q = newHandler;
				continue;
			}
			domNode.removeEventListener(key, oldCallback);
		}

		oldCallback = _VirtualDom_makeCallback(eventNode, newHandler);
		domNode.addEventListener(key, oldCallback,
			_VirtualDom_passiveSupported
			&& { passive: $elm$virtual_dom$VirtualDom$toHandlerInt(newHandler) < 2 }
		);
		allCallbacks[key] = oldCallback;
	}
}



// PASSIVE EVENTS


var _VirtualDom_passiveSupported;

try
{
	window.addEventListener('t', null, Object.defineProperty({}, 'passive', {
		get: function() { _VirtualDom_passiveSupported = true; }
	}));
}
catch(e) {}



// EVENT HANDLERS


function _VirtualDom_makeCallback(eventNode, initialHandler)
{
	function callback(event)
	{
		var handler = callback.q;
		var result = _Json_runHelp(handler.a, event);

		if (!$elm$core$Result$isOk(result))
		{
			return;
		}

		var tag = $elm$virtual_dom$VirtualDom$toHandlerInt(handler);

		// 0 = Normal
		// 1 = MayStopPropagation
		// 2 = MayPreventDefault
		// 3 = Custom

		var value = result.a;
		var message = !tag ? value : tag < 3 ? value.a : value.message;
		var stopPropagation = tag == 1 ? value.b : tag == 3 && value.stopPropagation;
		var currentEventNode = (
			stopPropagation && event.stopPropagation(),
			(tag == 2 ? value.b : tag == 3 && value.preventDefault) && event.preventDefault(),
			eventNode
		);
		var tagger;
		var i;
		while (tagger = currentEventNode.j)
		{
			if (typeof tagger == 'function')
			{
				message = tagger(message);
			}
			else
			{
				for (var i = tagger.length; i--; )
				{
					message = tagger[i](message);
				}
			}
			currentEventNode = currentEventNode.p;
		}
		currentEventNode(message, stopPropagation); // stopPropagation implies isSync
	}

	callback.q = initialHandler;

	return callback;
}

function _VirtualDom_equalEvents(x, y)
{
	return x.$ == y.$ && _Json_equality(x.a, y.a);
}



// DIFF


// TODO: Should we do patches like in iOS?
//
// type Patch
//   = At Int Patch
//   | Batch (List Patch)
//   | Change ...
//
// How could it not be better?
//
function _VirtualDom_diff(x, y)
{
	var patches = [];
	_VirtualDom_diffHelp(x, y, patches, 0);
	return patches;
}


function _VirtualDom_pushPatch(patches, type, index, data)
{
	var patch = {
		$: type,
		r: index,
		s: data,
		t: undefined,
		u: undefined
	};
	patches.push(patch);
	return patch;
}


function _VirtualDom_diffHelp(x, y, patches, index)
{
	if (x === y)
	{
		return;
	}

	var xType = x.$;
	var yType = y.$;

	// Bail if you run into different types of nodes. Implies that the
	// structure has changed significantly and it's not worth a diff.
	if (xType !== yType)
	{
		if (xType === 1 && yType === 2)
		{
			y = _VirtualDom_dekey(y);
			yType = 1;
		}
		else
		{
			_VirtualDom_pushPatch(patches, 0, index, y);
			return;
		}
	}

	// Now we know that both nodes are the same $.
	switch (yType)
	{
		case 5:
			var xRefs = x.l;
			var yRefs = y.l;
			var i = xRefs.length;
			var same = i === yRefs.length;
			while (same && i--)
			{
				same = xRefs[i] === yRefs[i];
			}
			if (same)
			{
				y.k = x.k;
				return;
			}
			y.k = y.m();
			var subPatches = [];
			_VirtualDom_diffHelp(x.k, y.k, subPatches, 0);
			subPatches.length > 0 && _VirtualDom_pushPatch(patches, 1, index, subPatches);
			return;

		case 4:
			// gather nested taggers
			var xTaggers = x.j;
			var yTaggers = y.j;
			var nesting = false;

			var xSubNode = x.k;
			while (xSubNode.$ === 4)
			{
				nesting = true;

				typeof xTaggers !== 'object'
					? xTaggers = [xTaggers, xSubNode.j]
					: xTaggers.push(xSubNode.j);

				xSubNode = xSubNode.k;
			}

			var ySubNode = y.k;
			while (ySubNode.$ === 4)
			{
				nesting = true;

				typeof yTaggers !== 'object'
					? yTaggers = [yTaggers, ySubNode.j]
					: yTaggers.push(ySubNode.j);

				ySubNode = ySubNode.k;
			}

			// Just bail if different numbers of taggers. This implies the
			// structure of the virtual DOM has changed.
			if (nesting && xTaggers.length !== yTaggers.length)
			{
				_VirtualDom_pushPatch(patches, 0, index, y);
				return;
			}

			// check if taggers are "the same"
			if (nesting ? !_VirtualDom_pairwiseRefEqual(xTaggers, yTaggers) : xTaggers !== yTaggers)
			{
				_VirtualDom_pushPatch(patches, 2, index, yTaggers);
			}

			// diff everything below the taggers
			_VirtualDom_diffHelp(xSubNode, ySubNode, patches, index + 1);
			return;

		case 0:
			if (x.a !== y.a)
			{
				_VirtualDom_pushPatch(patches, 3, index, y.a);
			}
			return;

		case 1:
			_VirtualDom_diffNodes(x, y, patches, index, _VirtualDom_diffKids);
			return;

		case 2:
			_VirtualDom_diffNodes(x, y, patches, index, _VirtualDom_diffKeyedKids);
			return;

		case 3:
			if (x.h !== y.h)
			{
				_VirtualDom_pushPatch(patches, 0, index, y);
				return;
			}

			var factsDiff = _VirtualDom_diffFacts(x.d, y.d);
			factsDiff && _VirtualDom_pushPatch(patches, 4, index, factsDiff);

			var patch = y.i(x.g, y.g);
			patch && _VirtualDom_pushPatch(patches, 5, index, patch);

			return;
	}
}

// assumes the incoming arrays are the same length
function _VirtualDom_pairwiseRefEqual(as, bs)
{
	for (var i = 0; i < as.length; i++)
	{
		if (as[i] !== bs[i])
		{
			return false;
		}
	}

	return true;
}

function _VirtualDom_diffNodes(x, y, patches, index, diffKids)
{
	// Bail if obvious indicators have changed. Implies more serious
	// structural changes such that it's not worth it to diff.
	if (x.c !== y.c || x.f !== y.f)
	{
		_VirtualDom_pushPatch(patches, 0, index, y);
		return;
	}

	var factsDiff = _VirtualDom_diffFacts(x.d, y.d);
	factsDiff && _VirtualDom_pushPatch(patches, 4, index, factsDiff);

	diffKids(x, y, patches, index);
}



// DIFF FACTS


// TODO Instead of creating a new diff object, it's possible to just test if
// there *is* a diff. During the actual patch, do the diff again and make the
// modifications directly. This way, there's no new allocations. Worth it?
function _VirtualDom_diffFacts(x, y, category)
{
	var diff;

	// look for changes and removals
	for (var xKey in x)
	{
		if (xKey === 'a1' || xKey === 'a0' || xKey === 'a3' || xKey === 'a4')
		{
			var subDiff = _VirtualDom_diffFacts(x[xKey], y[xKey] || {}, xKey);
			if (subDiff)
			{
				diff = diff || {};
				diff[xKey] = subDiff;
			}
			continue;
		}

		// remove if not in the new facts
		if (!(xKey in y))
		{
			diff = diff || {};
			diff[xKey] =
				!category
					? (typeof x[xKey] === 'string' ? '' : null)
					:
				(category === 'a1')
					? ''
					:
				(category === 'a0' || category === 'a3')
					? undefined
					:
				{ f: x[xKey].f, o: undefined };

			continue;
		}

		var xValue = x[xKey];
		var yValue = y[xKey];

		// reference equal, so don't worry about it
		if (xValue === yValue && xKey !== 'value' && xKey !== 'checked'
			|| category === 'a0' && _VirtualDom_equalEvents(xValue, yValue))
		{
			continue;
		}

		diff = diff || {};
		diff[xKey] = yValue;
	}

	// add new stuff
	for (var yKey in y)
	{
		if (!(yKey in x))
		{
			diff = diff || {};
			diff[yKey] = y[yKey];
		}
	}

	return diff;
}



// DIFF KIDS


function _VirtualDom_diffKids(xParent, yParent, patches, index)
{
	var xKids = xParent.e;
	var yKids = yParent.e;

	var xLen = xKids.length;
	var yLen = yKids.length;

	// FIGURE OUT IF THERE ARE INSERTS OR REMOVALS

	if (xLen > yLen)
	{
		_VirtualDom_pushPatch(patches, 6, index, {
			v: yLen,
			i: xLen - yLen
		});
	}
	else if (xLen < yLen)
	{
		_VirtualDom_pushPatch(patches, 7, index, {
			v: xLen,
			e: yKids
		});
	}

	// PAIRWISE DIFF EVERYTHING ELSE

	for (var minLen = xLen < yLen ? xLen : yLen, i = 0; i < minLen; i++)
	{
		var xKid = xKids[i];
		_VirtualDom_diffHelp(xKid, yKids[i], patches, ++index);
		index += xKid.b || 0;
	}
}



// KEYED DIFF


function _VirtualDom_diffKeyedKids(xParent, yParent, patches, rootIndex)
{
	var localPatches = [];

	var changes = {}; // Dict String Entry
	var inserts = []; // Array { index : Int, entry : Entry }
	// type Entry = { tag : String, vnode : VNode, index : Int, data : _ }

	var xKids = xParent.e;
	var yKids = yParent.e;
	var xLen = xKids.length;
	var yLen = yKids.length;
	var xIndex = 0;
	var yIndex = 0;

	var index = rootIndex;

	while (xIndex < xLen && yIndex < yLen)
	{
		var x = xKids[xIndex];
		var y = yKids[yIndex];

		var xKey = x.a;
		var yKey = y.a;
		var xNode = x.b;
		var yNode = y.b;

		var newMatch = undefined;
		var oldMatch = undefined;

		// check if keys match

		if (xKey === yKey)
		{
			index++;
			_VirtualDom_diffHelp(xNode, yNode, localPatches, index);
			index += xNode.b || 0;

			xIndex++;
			yIndex++;
			continue;
		}

		// look ahead 1 to detect insertions and removals.

		var xNext = xKids[xIndex + 1];
		var yNext = yKids[yIndex + 1];

		if (xNext)
		{
			var xNextKey = xNext.a;
			var xNextNode = xNext.b;
			oldMatch = yKey === xNextKey;
		}

		if (yNext)
		{
			var yNextKey = yNext.a;
			var yNextNode = yNext.b;
			newMatch = xKey === yNextKey;
		}


		// swap x and y
		if (newMatch && oldMatch)
		{
			index++;
			_VirtualDom_diffHelp(xNode, yNextNode, localPatches, index);
			_VirtualDom_insertNode(changes, localPatches, xKey, yNode, yIndex, inserts);
			index += xNode.b || 0;

			index++;
			_VirtualDom_removeNode(changes, localPatches, xKey, xNextNode, index);
			index += xNextNode.b || 0;

			xIndex += 2;
			yIndex += 2;
			continue;
		}

		// insert y
		if (newMatch)
		{
			index++;
			_VirtualDom_insertNode(changes, localPatches, yKey, yNode, yIndex, inserts);
			_VirtualDom_diffHelp(xNode, yNextNode, localPatches, index);
			index += xNode.b || 0;

			xIndex += 1;
			yIndex += 2;
			continue;
		}

		// remove x
		if (oldMatch)
		{
			index++;
			_VirtualDom_removeNode(changes, localPatches, xKey, xNode, index);
			index += xNode.b || 0;

			index++;
			_VirtualDom_diffHelp(xNextNode, yNode, localPatches, index);
			index += xNextNode.b || 0;

			xIndex += 2;
			yIndex += 1;
			continue;
		}

		// remove x, insert y
		if (xNext && xNextKey === yNextKey)
		{
			index++;
			_VirtualDom_removeNode(changes, localPatches, xKey, xNode, index);
			_VirtualDom_insertNode(changes, localPatches, yKey, yNode, yIndex, inserts);
			index += xNode.b || 0;

			index++;
			_VirtualDom_diffHelp(xNextNode, yNextNode, localPatches, index);
			index += xNextNode.b || 0;

			xIndex += 2;
			yIndex += 2;
			continue;
		}

		break;
	}

	// eat up any remaining nodes with removeNode and insertNode

	while (xIndex < xLen)
	{
		index++;
		var x = xKids[xIndex];
		var xNode = x.b;
		_VirtualDom_removeNode(changes, localPatches, x.a, xNode, index);
		index += xNode.b || 0;
		xIndex++;
	}

	while (yIndex < yLen)
	{
		var endInserts = endInserts || [];
		var y = yKids[yIndex];
		_VirtualDom_insertNode(changes, localPatches, y.a, y.b, undefined, endInserts);
		yIndex++;
	}

	if (localPatches.length > 0 || inserts.length > 0 || endInserts)
	{
		_VirtualDom_pushPatch(patches, 8, rootIndex, {
			w: localPatches,
			x: inserts,
			y: endInserts
		});
	}
}



// CHANGES FROM KEYED DIFF


var _VirtualDom_POSTFIX = '_elmW6BL';


function _VirtualDom_insertNode(changes, localPatches, key, vnode, yIndex, inserts)
{
	var entry = changes[key];

	// never seen this key before
	if (!entry)
	{
		entry = {
			c: 0,
			z: vnode,
			r: yIndex,
			s: undefined
		};

		inserts.push({ r: yIndex, A: entry });
		changes[key] = entry;

		return;
	}

	// this key was removed earlier, a match!
	if (entry.c === 1)
	{
		inserts.push({ r: yIndex, A: entry });

		entry.c = 2;
		var subPatches = [];
		_VirtualDom_diffHelp(entry.z, vnode, subPatches, entry.r);
		entry.r = yIndex;
		entry.s.s = {
			w: subPatches,
			A: entry
		};

		return;
	}

	// this key has already been inserted or moved, a duplicate!
	_VirtualDom_insertNode(changes, localPatches, key + _VirtualDom_POSTFIX, vnode, yIndex, inserts);
}


function _VirtualDom_removeNode(changes, localPatches, key, vnode, index)
{
	var entry = changes[key];

	// never seen this key before
	if (!entry)
	{
		var patch = _VirtualDom_pushPatch(localPatches, 9, index, undefined);

		changes[key] = {
			c: 1,
			z: vnode,
			r: index,
			s: patch
		};

		return;
	}

	// this key was inserted earlier, a match!
	if (entry.c === 0)
	{
		entry.c = 2;
		var subPatches = [];
		_VirtualDom_diffHelp(vnode, entry.z, subPatches, index);

		_VirtualDom_pushPatch(localPatches, 9, index, {
			w: subPatches,
			A: entry
		});

		return;
	}

	// this key has already been removed or moved, a duplicate!
	_VirtualDom_removeNode(changes, localPatches, key + _VirtualDom_POSTFIX, vnode, index);
}



// ADD DOM NODES
//
// Each DOM node has an "index" assigned in order of traversal. It is important
// to minimize our crawl over the actual DOM, so these indexes (along with the
// descendantsCount of virtual nodes) let us skip touching entire subtrees of
// the DOM if we know there are no patches there.


function _VirtualDom_addDomNodes(domNode, vNode, patches, eventNode)
{
	_VirtualDom_addDomNodesHelp(domNode, vNode, patches, 0, 0, vNode.b, eventNode);
}


// assumes `patches` is non-empty and indexes increase monotonically.
function _VirtualDom_addDomNodesHelp(domNode, vNode, patches, i, low, high, eventNode)
{
	var patch = patches[i];
	var index = patch.r;

	while (index === low)
	{
		var patchType = patch.$;

		if (patchType === 1)
		{
			_VirtualDom_addDomNodes(domNode, vNode.k, patch.s, eventNode);
		}
		else if (patchType === 8)
		{
			patch.t = domNode;
			patch.u = eventNode;

			var subPatches = patch.s.w;
			if (subPatches.length > 0)
			{
				_VirtualDom_addDomNodesHelp(domNode, vNode, subPatches, 0, low, high, eventNode);
			}
		}
		else if (patchType === 9)
		{
			patch.t = domNode;
			patch.u = eventNode;

			var data = patch.s;
			if (data)
			{
				data.A.s = domNode;
				var subPatches = data.w;
				if (subPatches.length > 0)
				{
					_VirtualDom_addDomNodesHelp(domNode, vNode, subPatches, 0, low, high, eventNode);
				}
			}
		}
		else
		{
			patch.t = domNode;
			patch.u = eventNode;
		}

		i++;

		if (!(patch = patches[i]) || (index = patch.r) > high)
		{
			return i;
		}
	}

	var tag = vNode.$;

	if (tag === 4)
	{
		var subNode = vNode.k;

		while (subNode.$ === 4)
		{
			subNode = subNode.k;
		}

		return _VirtualDom_addDomNodesHelp(domNode, subNode, patches, i, low + 1, high, domNode.elm_event_node_ref);
	}

	// tag must be 1 or 2 at this point

	var vKids = vNode.e;
	var childNodes = domNode.childNodes;
	for (var j = 0; j < vKids.length; j++)
	{
		low++;
		var vKid = tag === 1 ? vKids[j] : vKids[j].b;
		var nextLow = low + (vKid.b || 0);
		if (low <= index && index <= nextLow)
		{
			i = _VirtualDom_addDomNodesHelp(childNodes[j], vKid, patches, i, low, nextLow, eventNode);
			if (!(patch = patches[i]) || (index = patch.r) > high)
			{
				return i;
			}
		}
		low = nextLow;
	}
	return i;
}



// APPLY PATCHES


function _VirtualDom_applyPatches(rootDomNode, oldVirtualNode, patches, eventNode)
{
	if (patches.length === 0)
	{
		return rootDomNode;
	}

	_VirtualDom_addDomNodes(rootDomNode, oldVirtualNode, patches, eventNode);
	return _VirtualDom_applyPatchesHelp(rootDomNode, patches);
}

function _VirtualDom_applyPatchesHelp(rootDomNode, patches)
{
	for (var i = 0; i < patches.length; i++)
	{
		var patch = patches[i];
		var localDomNode = patch.t
		var newNode = _VirtualDom_applyPatch(localDomNode, patch);
		if (localDomNode === rootDomNode)
		{
			rootDomNode = newNode;
		}
	}
	return rootDomNode;
}

function _VirtualDom_applyPatch(domNode, patch)
{
	switch (patch.$)
	{
		case 0:
			return _VirtualDom_applyPatchRedraw(domNode, patch.s, patch.u);

		case 4:
			_VirtualDom_applyFacts(domNode, patch.u, patch.s);
			return domNode;

		case 3:
			domNode.replaceData(0, domNode.length, patch.s);
			return domNode;

		case 1:
			return _VirtualDom_applyPatchesHelp(domNode, patch.s);

		case 2:
			if (domNode.elm_event_node_ref)
			{
				domNode.elm_event_node_ref.j = patch.s;
			}
			else
			{
				domNode.elm_event_node_ref = { j: patch.s, p: patch.u };
			}
			return domNode;

		case 6:
			var data = patch.s;
			for (var i = 0; i < data.i; i++)
			{
				domNode.removeChild(domNode.childNodes[data.v]);
			}
			return domNode;

		case 7:
			var data = patch.s;
			var kids = data.e;
			var i = data.v;
			var theEnd = domNode.childNodes[i];
			for (; i < kids.length; i++)
			{
				domNode.insertBefore(_VirtualDom_render(kids[i], patch.u), theEnd);
			}
			return domNode;

		case 9:
			var data = patch.s;
			if (!data)
			{
				domNode.parentNode.removeChild(domNode);
				return domNode;
			}
			var entry = data.A;
			if (typeof entry.r !== 'undefined')
			{
				domNode.parentNode.removeChild(domNode);
			}
			entry.s = _VirtualDom_applyPatchesHelp(domNode, data.w);
			return domNode;

		case 8:
			return _VirtualDom_applyPatchReorder(domNode, patch);

		case 5:
			return patch.s(domNode);

		default:
			_Debug_crash(10); // 'Ran into an unknown patch!'
	}
}


function _VirtualDom_applyPatchRedraw(domNode, vNode, eventNode)
{
	var parentNode = domNode.parentNode;
	var newNode = _VirtualDom_render(vNode, eventNode);

	if (!newNode.elm_event_node_ref)
	{
		newNode.elm_event_node_ref = domNode.elm_event_node_ref;
	}

	if (parentNode && newNode !== domNode)
	{
		parentNode.replaceChild(newNode, domNode);
	}
	return newNode;
}


function _VirtualDom_applyPatchReorder(domNode, patch)
{
	var data = patch.s;

	// remove end inserts
	var frag = _VirtualDom_applyPatchReorderEndInsertsHelp(data.y, patch);

	// removals
	domNode = _VirtualDom_applyPatchesHelp(domNode, data.w);

	// inserts
	var inserts = data.x;
	for (var i = 0; i < inserts.length; i++)
	{
		var insert = inserts[i];
		var entry = insert.A;
		var node = entry.c === 2
			? entry.s
			: _VirtualDom_render(entry.z, patch.u);
		domNode.insertBefore(node, domNode.childNodes[insert.r]);
	}

	// add end inserts
	if (frag)
	{
		_VirtualDom_appendChild(domNode, frag);
	}

	return domNode;
}


function _VirtualDom_applyPatchReorderEndInsertsHelp(endInserts, patch)
{
	if (!endInserts)
	{
		return;
	}

	var frag = _VirtualDom_doc.createDocumentFragment();
	for (var i = 0; i < endInserts.length; i++)
	{
		var insert = endInserts[i];
		var entry = insert.A;
		_VirtualDom_appendChild(frag, entry.c === 2
			? entry.s
			: _VirtualDom_render(entry.z, patch.u)
		);
	}
	return frag;
}


function _VirtualDom_virtualize(node)
{
	// TEXT NODES

	if (node.nodeType === 3)
	{
		return _VirtualDom_text(node.textContent);
	}


	// WEIRD NODES

	if (node.nodeType !== 1)
	{
		return _VirtualDom_text('');
	}


	// ELEMENT NODES

	var attrList = _List_Nil;
	var attrs = node.attributes;
	for (var i = attrs.length; i--; )
	{
		var attr = attrs[i];
		var name = attr.name;
		var value = attr.value;
		attrList = _List_Cons( A2(_VirtualDom_attribute, name, value), attrList );
	}

	var tag = node.tagName.toLowerCase();
	var kidList = _List_Nil;
	var kids = node.childNodes;

	for (var i = kids.length; i--; )
	{
		kidList = _List_Cons(_VirtualDom_virtualize(kids[i]), kidList);
	}
	return A3(_VirtualDom_node, tag, attrList, kidList);
}

function _VirtualDom_dekey(keyedNode)
{
	var keyedKids = keyedNode.e;
	var len = keyedKids.length;
	var kids = new Array(len);
	for (var i = 0; i < len; i++)
	{
		kids[i] = keyedKids[i].b;
	}

	return {
		$: 1,
		c: keyedNode.c,
		d: keyedNode.d,
		e: kids,
		f: keyedNode.f,
		b: keyedNode.b
	};
}




// ELEMENT


var _Debugger_element;

var _Browser_element = _Debugger_element || F4(function(impl, flagDecoder, debugMetadata, args)
{
	return _Platform_initialize(
		flagDecoder,
		args,
		impl.init,
		impl.update,
		impl.subscriptions,
		function(sendToApp, initialModel) {
			var view = impl.view;
			/**_UNUSED/
			var domNode = args['node'];
			//*/
			/**/
			var domNode = args && args['node'] ? args['node'] : _Debug_crash(0);
			//*/
			var currNode = _VirtualDom_virtualize(domNode);

			return _Browser_makeAnimator(initialModel, function(model)
			{
				var nextNode = view(model);
				var patches = _VirtualDom_diff(currNode, nextNode);
				domNode = _VirtualDom_applyPatches(domNode, currNode, patches, sendToApp);
				currNode = nextNode;
			});
		}
	);
});



// DOCUMENT


var _Debugger_document;

var _Browser_document = _Debugger_document || F4(function(impl, flagDecoder, debugMetadata, args)
{
	return _Platform_initialize(
		flagDecoder,
		args,
		impl.init,
		impl.update,
		impl.subscriptions,
		function(sendToApp, initialModel) {
			var divertHrefToApp = impl.setup && impl.setup(sendToApp)
			var view = impl.view;
			var title = _VirtualDom_doc.title;
			var bodyNode = _VirtualDom_doc.body;
			var currNode = _VirtualDom_virtualize(bodyNode);
			return _Browser_makeAnimator(initialModel, function(model)
			{
				_VirtualDom_divertHrefToApp = divertHrefToApp;
				var doc = view(model);
				var nextNode = _VirtualDom_node('body')(_List_Nil)(doc.body);
				var patches = _VirtualDom_diff(currNode, nextNode);
				bodyNode = _VirtualDom_applyPatches(bodyNode, currNode, patches, sendToApp);
				currNode = nextNode;
				_VirtualDom_divertHrefToApp = 0;
				(title !== doc.title) && (_VirtualDom_doc.title = title = doc.title);
			});
		}
	);
});



// ANIMATION


var _Browser_cancelAnimationFrame =
	typeof cancelAnimationFrame !== 'undefined'
		? cancelAnimationFrame
		: function(id) { clearTimeout(id); };

var _Browser_requestAnimationFrame =
	typeof requestAnimationFrame !== 'undefined'
		? requestAnimationFrame
		: function(callback) { return setTimeout(callback, 1000 / 60); };


function _Browser_makeAnimator(model, draw)
{
	draw(model);

	var state = 0;

	function updateIfNeeded()
	{
		state = state === 1
			? 0
			: ( _Browser_requestAnimationFrame(updateIfNeeded), draw(model), 1 );
	}

	return function(nextModel, isSync)
	{
		model = nextModel;

		isSync
			? ( draw(model),
				state === 2 && (state = 1)
				)
			: ( state === 0 && _Browser_requestAnimationFrame(updateIfNeeded),
				state = 2
				);
	};
}



// APPLICATION


function _Browser_application(impl)
{
	var onUrlChange = impl.onUrlChange;
	var onUrlRequest = impl.onUrlRequest;
	var key = function() { key.a(onUrlChange(_Browser_getUrl())); };

	return _Browser_document({
		setup: function(sendToApp)
		{
			key.a = sendToApp;
			_Browser_window.addEventListener('popstate', key);
			_Browser_window.navigator.userAgent.indexOf('Trident') < 0 || _Browser_window.addEventListener('hashchange', key);

			return F2(function(domNode, event)
			{
				if (!event.ctrlKey && !event.metaKey && !event.shiftKey && event.button < 1 && !domNode.target && !domNode.hasAttribute('download'))
				{
					event.preventDefault();
					var href = domNode.href;
					var curr = _Browser_getUrl();
					var next = $elm$url$Url$fromString(href).a;
					sendToApp(onUrlRequest(
						(next
							&& curr.protocol === next.protocol
							&& curr.host === next.host
							&& curr.port_.a === next.port_.a
						)
							? $elm$browser$Browser$Internal(next)
							: $elm$browser$Browser$External(href)
					));
				}
			});
		},
		init: function(flags)
		{
			return A3(impl.init, flags, _Browser_getUrl(), key);
		},
		view: impl.view,
		update: impl.update,
		subscriptions: impl.subscriptions
	});
}

function _Browser_getUrl()
{
	return $elm$url$Url$fromString(_VirtualDom_doc.location.href).a || _Debug_crash(1);
}

var _Browser_go = F2(function(key, n)
{
	return A2($elm$core$Task$perform, $elm$core$Basics$never, _Scheduler_binding(function() {
		n && history.go(n);
		key();
	}));
});

var _Browser_pushUrl = F2(function(key, url)
{
	return A2($elm$core$Task$perform, $elm$core$Basics$never, _Scheduler_binding(function() {
		history.pushState({}, '', url);
		key();
	}));
});

var _Browser_replaceUrl = F2(function(key, url)
{
	return A2($elm$core$Task$perform, $elm$core$Basics$never, _Scheduler_binding(function() {
		history.replaceState({}, '', url);
		key();
	}));
});



// GLOBAL EVENTS


var _Browser_fakeNode = { addEventListener: function() {}, removeEventListener: function() {} };
var _Browser_doc = typeof document !== 'undefined' ? document : _Browser_fakeNode;
var _Browser_window = typeof window !== 'undefined' ? window : _Browser_fakeNode;

var _Browser_on = F3(function(node, eventName, sendToSelf)
{
	return _Scheduler_spawn(_Scheduler_binding(function(callback)
	{
		function handler(event)	{ _Scheduler_rawSpawn(sendToSelf(event)); }
		node.addEventListener(eventName, handler, _VirtualDom_passiveSupported && { passive: true });
		return function() { node.removeEventListener(eventName, handler); };
	}));
});

var _Browser_decodeEvent = F2(function(decoder, event)
{
	var result = _Json_runHelp(decoder, event);
	return $elm$core$Result$isOk(result) ? $elm$core$Maybe$Just(result.a) : $elm$core$Maybe$Nothing;
});



// PAGE VISIBILITY


function _Browser_visibilityInfo()
{
	return (typeof _VirtualDom_doc.hidden !== 'undefined')
		? { hidden: 'hidden', change: 'visibilitychange' }
		:
	(typeof _VirtualDom_doc.mozHidden !== 'undefined')
		? { hidden: 'mozHidden', change: 'mozvisibilitychange' }
		:
	(typeof _VirtualDom_doc.msHidden !== 'undefined')
		? { hidden: 'msHidden', change: 'msvisibilitychange' }
		:
	(typeof _VirtualDom_doc.webkitHidden !== 'undefined')
		? { hidden: 'webkitHidden', change: 'webkitvisibilitychange' }
		: { hidden: 'hidden', change: 'visibilitychange' };
}



// ANIMATION FRAMES


function _Browser_rAF()
{
	return _Scheduler_binding(function(callback)
	{
		var id = _Browser_requestAnimationFrame(function() {
			callback(_Scheduler_succeed(Date.now()));
		});

		return function() {
			_Browser_cancelAnimationFrame(id);
		};
	});
}


function _Browser_now()
{
	return _Scheduler_binding(function(callback)
	{
		callback(_Scheduler_succeed(Date.now()));
	});
}



// DOM STUFF


function _Browser_withNode(id, doStuff)
{
	return _Scheduler_binding(function(callback)
	{
		_Browser_requestAnimationFrame(function() {
			var node = document.getElementById(id);
			callback(node
				? _Scheduler_succeed(doStuff(node))
				: _Scheduler_fail($elm$browser$Browser$Dom$NotFound(id))
			);
		});
	});
}


function _Browser_withWindow(doStuff)
{
	return _Scheduler_binding(function(callback)
	{
		_Browser_requestAnimationFrame(function() {
			callback(_Scheduler_succeed(doStuff()));
		});
	});
}


// FOCUS and BLUR


var _Browser_call = F2(function(functionName, id)
{
	return _Browser_withNode(id, function(node) {
		node[functionName]();
		return _Utils_Tuple0;
	});
});



// WINDOW VIEWPORT


function _Browser_getViewport()
{
	return {
		scene: _Browser_getScene(),
		viewport: {
			x: _Browser_window.pageXOffset,
			y: _Browser_window.pageYOffset,
			width: _Browser_doc.documentElement.clientWidth,
			height: _Browser_doc.documentElement.clientHeight
		}
	};
}

function _Browser_getScene()
{
	var body = _Browser_doc.body;
	var elem = _Browser_doc.documentElement;
	return {
		width: Math.max(body.scrollWidth, body.offsetWidth, elem.scrollWidth, elem.offsetWidth, elem.clientWidth),
		height: Math.max(body.scrollHeight, body.offsetHeight, elem.scrollHeight, elem.offsetHeight, elem.clientHeight)
	};
}

var _Browser_setViewport = F2(function(x, y)
{
	return _Browser_withWindow(function()
	{
		_Browser_window.scroll(x, y);
		return _Utils_Tuple0;
	});
});



// ELEMENT VIEWPORT


function _Browser_getViewportOf(id)
{
	return _Browser_withNode(id, function(node)
	{
		return {
			scene: {
				width: node.scrollWidth,
				height: node.scrollHeight
			},
			viewport: {
				x: node.scrollLeft,
				y: node.scrollTop,
				width: node.clientWidth,
				height: node.clientHeight
			}
		};
	});
}


var _Browser_setViewportOf = F3(function(id, x, y)
{
	return _Browser_withNode(id, function(node)
	{
		node.scrollLeft = x;
		node.scrollTop = y;
		return _Utils_Tuple0;
	});
});



// ELEMENT


function _Browser_getElement(id)
{
	return _Browser_withNode(id, function(node)
	{
		var rect = node.getBoundingClientRect();
		var x = _Browser_window.pageXOffset;
		var y = _Browser_window.pageYOffset;
		return {
			scene: _Browser_getScene(),
			viewport: {
				x: x,
				y: y,
				width: _Browser_doc.documentElement.clientWidth,
				height: _Browser_doc.documentElement.clientHeight
			},
			element: {
				x: x + rect.left,
				y: y + rect.top,
				width: rect.width,
				height: rect.height
			}
		};
	});
}



// LOAD and RELOAD


function _Browser_reload(skipCache)
{
	return A2($elm$core$Task$perform, $elm$core$Basics$never, _Scheduler_binding(function(callback)
	{
		_VirtualDom_doc.location.reload(skipCache);
	}));
}

function _Browser_load(url)
{
	return A2($elm$core$Task$perform, $elm$core$Basics$never, _Scheduler_binding(function(callback)
	{
		try
		{
			_Browser_window.location = url;
		}
		catch(err)
		{
			// Only Firefox can throw a NS_ERROR_MALFORMED_URI exception here.
			// Other browsers reload the page, so let's be consistent about that.
			_VirtualDom_doc.location.reload(false);
		}
	}));
}


/*
 * Copyright (c) 2010 Mozilla Corporation
 * Copyright (c) 2010 Vladimir Vukicevic
 * Copyright (c) 2013 John Mayer
 * Copyright (c) 2018 Andrey Kuzmin
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

// Vector2

var _MJS_v2 = F2(function(x, y) {
    return new Float64Array([x, y]);
});

var _MJS_v2getX = function(a) {
    return a[0];
};

var _MJS_v2getY = function(a) {
    return a[1];
};

var _MJS_v2setX = F2(function(x, a) {
    return new Float64Array([x, a[1]]);
});

var _MJS_v2setY = F2(function(y, a) {
    return new Float64Array([a[0], y]);
});

var _MJS_v2toRecord = function(a) {
    return { x: a[0], y: a[1] };
};

var _MJS_v2fromRecord = function(r) {
    return new Float64Array([r.x, r.y]);
};

var _MJS_v2add = F2(function(a, b) {
    var r = new Float64Array(2);
    r[0] = a[0] + b[0];
    r[1] = a[1] + b[1];
    return r;
});

var _MJS_v2sub = F2(function(a, b) {
    var r = new Float64Array(2);
    r[0] = a[0] - b[0];
    r[1] = a[1] - b[1];
    return r;
});

var _MJS_v2negate = function(a) {
    var r = new Float64Array(2);
    r[0] = -a[0];
    r[1] = -a[1];
    return r;
};

var _MJS_v2direction = F2(function(a, b) {
    var r = new Float64Array(2);
    r[0] = a[0] - b[0];
    r[1] = a[1] - b[1];
    var im = 1.0 / _MJS_v2lengthLocal(r);
    r[0] = r[0] * im;
    r[1] = r[1] * im;
    return r;
});

function _MJS_v2lengthLocal(a) {
    return Math.sqrt(a[0] * a[0] + a[1] * a[1]);
}
var _MJS_v2length = _MJS_v2lengthLocal;

var _MJS_v2lengthSquared = function(a) {
    return a[0] * a[0] + a[1] * a[1];
};

var _MJS_v2distance = F2(function(a, b) {
    var dx = a[0] - b[0];
    var dy = a[1] - b[1];
    return Math.sqrt(dx * dx + dy * dy);
});

var _MJS_v2distanceSquared = F2(function(a, b) {
    var dx = a[0] - b[0];
    var dy = a[1] - b[1];
    return dx * dx + dy * dy;
});

var _MJS_v2normalize = function(a) {
    var r = new Float64Array(2);
    var im = 1.0 / _MJS_v2lengthLocal(a);
    r[0] = a[0] * im;
    r[1] = a[1] * im;
    return r;
};

var _MJS_v2scale = F2(function(k, a) {
    var r = new Float64Array(2);
    r[0] = a[0] * k;
    r[1] = a[1] * k;
    return r;
});

var _MJS_v2dot = F2(function(a, b) {
    return a[0] * b[0] + a[1] * b[1];
});

// Vector3

var _MJS_v3temp1Local = new Float64Array(3);
var _MJS_v3temp2Local = new Float64Array(3);
var _MJS_v3temp3Local = new Float64Array(3);

var _MJS_v3 = F3(function(x, y, z) {
    return new Float64Array([x, y, z]);
});

var _MJS_v3getX = function(a) {
    return a[0];
};

var _MJS_v3getY = function(a) {
    return a[1];
};

var _MJS_v3getZ = function(a) {
    return a[2];
};

var _MJS_v3setX = F2(function(x, a) {
    return new Float64Array([x, a[1], a[2]]);
});

var _MJS_v3setY = F2(function(y, a) {
    return new Float64Array([a[0], y, a[2]]);
});

var _MJS_v3setZ = F2(function(z, a) {
    return new Float64Array([a[0], a[1], z]);
});

var _MJS_v3toRecord = function(a) {
    return { x: a[0], y: a[1], z: a[2] };
};

var _MJS_v3fromRecord = function(r) {
    return new Float64Array([r.x, r.y, r.z]);
};

var _MJS_v3add = F2(function(a, b) {
    var r = new Float64Array(3);
    r[0] = a[0] + b[0];
    r[1] = a[1] + b[1];
    r[2] = a[2] + b[2];
    return r;
});

function _MJS_v3subLocal(a, b, r) {
    if (r === undefined) {
        r = new Float64Array(3);
    }
    r[0] = a[0] - b[0];
    r[1] = a[1] - b[1];
    r[2] = a[2] - b[2];
    return r;
}
var _MJS_v3sub = F2(_MJS_v3subLocal);

var _MJS_v3negate = function(a) {
    var r = new Float64Array(3);
    r[0] = -a[0];
    r[1] = -a[1];
    r[2] = -a[2];
    return r;
};

function _MJS_v3directionLocal(a, b, r) {
    if (r === undefined) {
        r = new Float64Array(3);
    }
    return _MJS_v3normalizeLocal(_MJS_v3subLocal(a, b, r), r);
}
var _MJS_v3direction = F2(_MJS_v3directionLocal);

function _MJS_v3lengthLocal(a) {
    return Math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);
}
var _MJS_v3length = _MJS_v3lengthLocal;

var _MJS_v3lengthSquared = function(a) {
    return a[0] * a[0] + a[1] * a[1] + a[2] * a[2];
};

var _MJS_v3distance = F2(function(a, b) {
    var dx = a[0] - b[0];
    var dy = a[1] - b[1];
    var dz = a[2] - b[2];
    return Math.sqrt(dx * dx + dy * dy + dz * dz);
});

var _MJS_v3distanceSquared = F2(function(a, b) {
    var dx = a[0] - b[0];
    var dy = a[1] - b[1];
    var dz = a[2] - b[2];
    return dx * dx + dy * dy + dz * dz;
});

function _MJS_v3normalizeLocal(a, r) {
    if (r === undefined) {
        r = new Float64Array(3);
    }
    var im = 1.0 / _MJS_v3lengthLocal(a);
    r[0] = a[0] * im;
    r[1] = a[1] * im;
    r[2] = a[2] * im;
    return r;
}
var _MJS_v3normalize = _MJS_v3normalizeLocal;

var _MJS_v3scale = F2(function(k, a) {
    return new Float64Array([a[0] * k, a[1] * k, a[2] * k]);
});

var _MJS_v3dotLocal = function(a, b) {
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
};
var _MJS_v3dot = F2(_MJS_v3dotLocal);

function _MJS_v3crossLocal(a, b, r) {
    if (r === undefined) {
        r = new Float64Array(3);
    }
    r[0] = a[1] * b[2] - a[2] * b[1];
    r[1] = a[2] * b[0] - a[0] * b[2];
    r[2] = a[0] * b[1] - a[1] * b[0];
    return r;
}
var _MJS_v3cross = F2(_MJS_v3crossLocal);

var _MJS_v3mul4x4 = F2(function(m, v) {
    var w;
    var tmp = _MJS_v3temp1Local;
    var r = new Float64Array(3);

    tmp[0] = m[3];
    tmp[1] = m[7];
    tmp[2] = m[11];
    w = _MJS_v3dotLocal(v, tmp) + m[15];
    tmp[0] = m[0];
    tmp[1] = m[4];
    tmp[2] = m[8];
    r[0] = (_MJS_v3dotLocal(v, tmp) + m[12]) / w;
    tmp[0] = m[1];
    tmp[1] = m[5];
    tmp[2] = m[9];
    r[1] = (_MJS_v3dotLocal(v, tmp) + m[13]) / w;
    tmp[0] = m[2];
    tmp[1] = m[6];
    tmp[2] = m[10];
    r[2] = (_MJS_v3dotLocal(v, tmp) + m[14]) / w;
    return r;
});

// Vector4

var _MJS_v4 = F4(function(x, y, z, w) {
    return new Float64Array([x, y, z, w]);
});

var _MJS_v4getX = function(a) {
    return a[0];
};

var _MJS_v4getY = function(a) {
    return a[1];
};

var _MJS_v4getZ = function(a) {
    return a[2];
};

var _MJS_v4getW = function(a) {
    return a[3];
};

var _MJS_v4setX = F2(function(x, a) {
    return new Float64Array([x, a[1], a[2], a[3]]);
});

var _MJS_v4setY = F2(function(y, a) {
    return new Float64Array([a[0], y, a[2], a[3]]);
});

var _MJS_v4setZ = F2(function(z, a) {
    return new Float64Array([a[0], a[1], z, a[3]]);
});

var _MJS_v4setW = F2(function(w, a) {
    return new Float64Array([a[0], a[1], a[2], w]);
});

var _MJS_v4toRecord = function(a) {
    return { x: a[0], y: a[1], z: a[2], w: a[3] };
};

var _MJS_v4fromRecord = function(r) {
    return new Float64Array([r.x, r.y, r.z, r.w]);
};

var _MJS_v4add = F2(function(a, b) {
    var r = new Float64Array(4);
    r[0] = a[0] + b[0];
    r[1] = a[1] + b[1];
    r[2] = a[2] + b[2];
    r[3] = a[3] + b[3];
    return r;
});

var _MJS_v4sub = F2(function(a, b) {
    var r = new Float64Array(4);
    r[0] = a[0] - b[0];
    r[1] = a[1] - b[1];
    r[2] = a[2] - b[2];
    r[3] = a[3] - b[3];
    return r;
});

var _MJS_v4negate = function(a) {
    var r = new Float64Array(4);
    r[0] = -a[0];
    r[1] = -a[1];
    r[2] = -a[2];
    r[3] = -a[3];
    return r;
};

var _MJS_v4direction = F2(function(a, b) {
    var r = new Float64Array(4);
    r[0] = a[0] - b[0];
    r[1] = a[1] - b[1];
    r[2] = a[2] - b[2];
    r[3] = a[3] - b[3];
    var im = 1.0 / _MJS_v4lengthLocal(r);
    r[0] = r[0] * im;
    r[1] = r[1] * im;
    r[2] = r[2] * im;
    r[3] = r[3] * im;
    return r;
});

function _MJS_v4lengthLocal(a) {
    return Math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2] + a[3] * a[3]);
}
var _MJS_v4length = _MJS_v4lengthLocal;

var _MJS_v4lengthSquared = function(a) {
    return a[0] * a[0] + a[1] * a[1] + a[2] * a[2] + a[3] * a[3];
};

var _MJS_v4distance = F2(function(a, b) {
    var dx = a[0] - b[0];
    var dy = a[1] - b[1];
    var dz = a[2] - b[2];
    var dw = a[3] - b[3];
    return Math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw);
});

var _MJS_v4distanceSquared = F2(function(a, b) {
    var dx = a[0] - b[0];
    var dy = a[1] - b[1];
    var dz = a[2] - b[2];
    var dw = a[3] - b[3];
    return dx * dx + dy * dy + dz * dz + dw * dw;
});

var _MJS_v4normalize = function(a) {
    var r = new Float64Array(4);
    var im = 1.0 / _MJS_v4lengthLocal(a);
    r[0] = a[0] * im;
    r[1] = a[1] * im;
    r[2] = a[2] * im;
    r[3] = a[3] * im;
    return r;
};

var _MJS_v4scale = F2(function(k, a) {
    var r = new Float64Array(4);
    r[0] = a[0] * k;
    r[1] = a[1] * k;
    r[2] = a[2] * k;
    r[3] = a[3] * k;
    return r;
});

var _MJS_v4dot = F2(function(a, b) {
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3];
});

// Matrix4

var _MJS_m4x4temp1Local = new Float64Array(16);
var _MJS_m4x4temp2Local = new Float64Array(16);

var _MJS_m4x4identity = new Float64Array([
    1.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 1.0
]);

var _MJS_m4x4fromRecord = function(r) {
    var m = new Float64Array(16);
    m[0] = r.m11;
    m[1] = r.m21;
    m[2] = r.m31;
    m[3] = r.m41;
    m[4] = r.m12;
    m[5] = r.m22;
    m[6] = r.m32;
    m[7] = r.m42;
    m[8] = r.m13;
    m[9] = r.m23;
    m[10] = r.m33;
    m[11] = r.m43;
    m[12] = r.m14;
    m[13] = r.m24;
    m[14] = r.m34;
    m[15] = r.m44;
    return m;
};

var _MJS_m4x4toRecord = function(m) {
    return {
        m11: m[0], m21: m[1], m31: m[2], m41: m[3],
        m12: m[4], m22: m[5], m32: m[6], m42: m[7],
        m13: m[8], m23: m[9], m33: m[10], m43: m[11],
        m14: m[12], m24: m[13], m34: m[14], m44: m[15]
    };
};

var _MJS_m4x4inverse = function(m) {
    var r = new Float64Array(16);

    r[0] = m[5] * m[10] * m[15] - m[5] * m[11] * m[14] - m[9] * m[6] * m[15] +
        m[9] * m[7] * m[14] + m[13] * m[6] * m[11] - m[13] * m[7] * m[10];
    r[4] = -m[4] * m[10] * m[15] + m[4] * m[11] * m[14] + m[8] * m[6] * m[15] -
        m[8] * m[7] * m[14] - m[12] * m[6] * m[11] + m[12] * m[7] * m[10];
    r[8] = m[4] * m[9] * m[15] - m[4] * m[11] * m[13] - m[8] * m[5] * m[15] +
        m[8] * m[7] * m[13] + m[12] * m[5] * m[11] - m[12] * m[7] * m[9];
    r[12] = -m[4] * m[9] * m[14] + m[4] * m[10] * m[13] + m[8] * m[5] * m[14] -
        m[8] * m[6] * m[13] - m[12] * m[5] * m[10] + m[12] * m[6] * m[9];
    r[1] = -m[1] * m[10] * m[15] + m[1] * m[11] * m[14] + m[9] * m[2] * m[15] -
        m[9] * m[3] * m[14] - m[13] * m[2] * m[11] + m[13] * m[3] * m[10];
    r[5] = m[0] * m[10] * m[15] - m[0] * m[11] * m[14] - m[8] * m[2] * m[15] +
        m[8] * m[3] * m[14] + m[12] * m[2] * m[11] - m[12] * m[3] * m[10];
    r[9] = -m[0] * m[9] * m[15] + m[0] * m[11] * m[13] + m[8] * m[1] * m[15] -
        m[8] * m[3] * m[13] - m[12] * m[1] * m[11] + m[12] * m[3] * m[9];
    r[13] = m[0] * m[9] * m[14] - m[0] * m[10] * m[13] - m[8] * m[1] * m[14] +
        m[8] * m[2] * m[13] + m[12] * m[1] * m[10] - m[12] * m[2] * m[9];
    r[2] = m[1] * m[6] * m[15] - m[1] * m[7] * m[14] - m[5] * m[2] * m[15] +
        m[5] * m[3] * m[14] + m[13] * m[2] * m[7] - m[13] * m[3] * m[6];
    r[6] = -m[0] * m[6] * m[15] + m[0] * m[7] * m[14] + m[4] * m[2] * m[15] -
        m[4] * m[3] * m[14] - m[12] * m[2] * m[7] + m[12] * m[3] * m[6];
    r[10] = m[0] * m[5] * m[15] - m[0] * m[7] * m[13] - m[4] * m[1] * m[15] +
        m[4] * m[3] * m[13] + m[12] * m[1] * m[7] - m[12] * m[3] * m[5];
    r[14] = -m[0] * m[5] * m[14] + m[0] * m[6] * m[13] + m[4] * m[1] * m[14] -
        m[4] * m[2] * m[13] - m[12] * m[1] * m[6] + m[12] * m[2] * m[5];
    r[3] = -m[1] * m[6] * m[11] + m[1] * m[7] * m[10] + m[5] * m[2] * m[11] -
        m[5] * m[3] * m[10] - m[9] * m[2] * m[7] + m[9] * m[3] * m[6];
    r[7] = m[0] * m[6] * m[11] - m[0] * m[7] * m[10] - m[4] * m[2] * m[11] +
        m[4] * m[3] * m[10] + m[8] * m[2] * m[7] - m[8] * m[3] * m[6];
    r[11] = -m[0] * m[5] * m[11] + m[0] * m[7] * m[9] + m[4] * m[1] * m[11] -
        m[4] * m[3] * m[9] - m[8] * m[1] * m[7] + m[8] * m[3] * m[5];
    r[15] = m[0] * m[5] * m[10] - m[0] * m[6] * m[9] - m[4] * m[1] * m[10] +
        m[4] * m[2] * m[9] + m[8] * m[1] * m[6] - m[8] * m[2] * m[5];

    var det = m[0] * r[0] + m[1] * r[4] + m[2] * r[8] + m[3] * r[12];

    if (det === 0) {
        return $elm$core$Maybe$Nothing;
    }

    det = 1.0 / det;

    for (var i = 0; i < 16; i = i + 1) {
        r[i] = r[i] * det;
    }

    return $elm$core$Maybe$Just(r);
};

var _MJS_m4x4inverseOrthonormal = function(m) {
    var r = _MJS_m4x4transposeLocal(m);
    var t = [m[12], m[13], m[14]];
    r[3] = r[7] = r[11] = 0;
    r[12] = -_MJS_v3dotLocal([r[0], r[4], r[8]], t);
    r[13] = -_MJS_v3dotLocal([r[1], r[5], r[9]], t);
    r[14] = -_MJS_v3dotLocal([r[2], r[6], r[10]], t);
    return r;
};

function _MJS_m4x4makeFrustumLocal(left, right, bottom, top, znear, zfar) {
    var r = new Float64Array(16);

    r[0] = 2 * znear / (right - left);
    r[1] = 0;
    r[2] = 0;
    r[3] = 0;
    r[4] = 0;
    r[5] = 2 * znear / (top - bottom);
    r[6] = 0;
    r[7] = 0;
    r[8] = (right + left) / (right - left);
    r[9] = (top + bottom) / (top - bottom);
    r[10] = -(zfar + znear) / (zfar - znear);
    r[11] = -1;
    r[12] = 0;
    r[13] = 0;
    r[14] = -2 * zfar * znear / (zfar - znear);
    r[15] = 0;

    return r;
}
var _MJS_m4x4makeFrustum = F6(_MJS_m4x4makeFrustumLocal);

var _MJS_m4x4makePerspective = F4(function(fovy, aspect, znear, zfar) {
    var ymax = znear * Math.tan(fovy * Math.PI / 360.0);
    var ymin = -ymax;
    var xmin = ymin * aspect;
    var xmax = ymax * aspect;

    return _MJS_m4x4makeFrustumLocal(xmin, xmax, ymin, ymax, znear, zfar);
});

function _MJS_m4x4makeOrthoLocal(left, right, bottom, top, znear, zfar) {
    var r = new Float64Array(16);

    r[0] = 2 / (right - left);
    r[1] = 0;
    r[2] = 0;
    r[3] = 0;
    r[4] = 0;
    r[5] = 2 / (top - bottom);
    r[6] = 0;
    r[7] = 0;
    r[8] = 0;
    r[9] = 0;
    r[10] = -2 / (zfar - znear);
    r[11] = 0;
    r[12] = -(right + left) / (right - left);
    r[13] = -(top + bottom) / (top - bottom);
    r[14] = -(zfar + znear) / (zfar - znear);
    r[15] = 1;

    return r;
}
var _MJS_m4x4makeOrtho = F6(_MJS_m4x4makeOrthoLocal);

var _MJS_m4x4makeOrtho2D = F4(function(left, right, bottom, top) {
    return _MJS_m4x4makeOrthoLocal(left, right, bottom, top, -1, 1);
});

function _MJS_m4x4mulLocal(a, b) {
    var r = new Float64Array(16);
    var a11 = a[0];
    var a21 = a[1];
    var a31 = a[2];
    var a41 = a[3];
    var a12 = a[4];
    var a22 = a[5];
    var a32 = a[6];
    var a42 = a[7];
    var a13 = a[8];
    var a23 = a[9];
    var a33 = a[10];
    var a43 = a[11];
    var a14 = a[12];
    var a24 = a[13];
    var a34 = a[14];
    var a44 = a[15];
    var b11 = b[0];
    var b21 = b[1];
    var b31 = b[2];
    var b41 = b[3];
    var b12 = b[4];
    var b22 = b[5];
    var b32 = b[6];
    var b42 = b[7];
    var b13 = b[8];
    var b23 = b[9];
    var b33 = b[10];
    var b43 = b[11];
    var b14 = b[12];
    var b24 = b[13];
    var b34 = b[14];
    var b44 = b[15];

    r[0] = a11 * b11 + a12 * b21 + a13 * b31 + a14 * b41;
    r[1] = a21 * b11 + a22 * b21 + a23 * b31 + a24 * b41;
    r[2] = a31 * b11 + a32 * b21 + a33 * b31 + a34 * b41;
    r[3] = a41 * b11 + a42 * b21 + a43 * b31 + a44 * b41;
    r[4] = a11 * b12 + a12 * b22 + a13 * b32 + a14 * b42;
    r[5] = a21 * b12 + a22 * b22 + a23 * b32 + a24 * b42;
    r[6] = a31 * b12 + a32 * b22 + a33 * b32 + a34 * b42;
    r[7] = a41 * b12 + a42 * b22 + a43 * b32 + a44 * b42;
    r[8] = a11 * b13 + a12 * b23 + a13 * b33 + a14 * b43;
    r[9] = a21 * b13 + a22 * b23 + a23 * b33 + a24 * b43;
    r[10] = a31 * b13 + a32 * b23 + a33 * b33 + a34 * b43;
    r[11] = a41 * b13 + a42 * b23 + a43 * b33 + a44 * b43;
    r[12] = a11 * b14 + a12 * b24 + a13 * b34 + a14 * b44;
    r[13] = a21 * b14 + a22 * b24 + a23 * b34 + a24 * b44;
    r[14] = a31 * b14 + a32 * b24 + a33 * b34 + a34 * b44;
    r[15] = a41 * b14 + a42 * b24 + a43 * b34 + a44 * b44;

    return r;
}
var _MJS_m4x4mul = F2(_MJS_m4x4mulLocal);

var _MJS_m4x4mulAffine = F2(function(a, b) {
    var r = new Float64Array(16);
    var a11 = a[0];
    var a21 = a[1];
    var a31 = a[2];
    var a12 = a[4];
    var a22 = a[5];
    var a32 = a[6];
    var a13 = a[8];
    var a23 = a[9];
    var a33 = a[10];
    var a14 = a[12];
    var a24 = a[13];
    var a34 = a[14];

    var b11 = b[0];
    var b21 = b[1];
    var b31 = b[2];
    var b12 = b[4];
    var b22 = b[5];
    var b32 = b[6];
    var b13 = b[8];
    var b23 = b[9];
    var b33 = b[10];
    var b14 = b[12];
    var b24 = b[13];
    var b34 = b[14];

    r[0] = a11 * b11 + a12 * b21 + a13 * b31;
    r[1] = a21 * b11 + a22 * b21 + a23 * b31;
    r[2] = a31 * b11 + a32 * b21 + a33 * b31;
    r[3] = 0;
    r[4] = a11 * b12 + a12 * b22 + a13 * b32;
    r[5] = a21 * b12 + a22 * b22 + a23 * b32;
    r[6] = a31 * b12 + a32 * b22 + a33 * b32;
    r[7] = 0;
    r[8] = a11 * b13 + a12 * b23 + a13 * b33;
    r[9] = a21 * b13 + a22 * b23 + a23 * b33;
    r[10] = a31 * b13 + a32 * b23 + a33 * b33;
    r[11] = 0;
    r[12] = a11 * b14 + a12 * b24 + a13 * b34 + a14;
    r[13] = a21 * b14 + a22 * b24 + a23 * b34 + a24;
    r[14] = a31 * b14 + a32 * b24 + a33 * b34 + a34;
    r[15] = 1;

    return r;
});

var _MJS_m4x4makeRotate = F2(function(angle, axis) {
    var r = new Float64Array(16);
    axis = _MJS_v3normalizeLocal(axis, _MJS_v3temp1Local);
    var x = axis[0];
    var y = axis[1];
    var z = axis[2];
    var c = Math.cos(angle);
    var c1 = 1 - c;
    var s = Math.sin(angle);

    r[0] = x * x * c1 + c;
    r[1] = y * x * c1 + z * s;
    r[2] = z * x * c1 - y * s;
    r[3] = 0;
    r[4] = x * y * c1 - z * s;
    r[5] = y * y * c1 + c;
    r[6] = y * z * c1 + x * s;
    r[7] = 0;
    r[8] = x * z * c1 + y * s;
    r[9] = y * z * c1 - x * s;
    r[10] = z * z * c1 + c;
    r[11] = 0;
    r[12] = 0;
    r[13] = 0;
    r[14] = 0;
    r[15] = 1;

    return r;
});

var _MJS_m4x4rotate = F3(function(angle, axis, m) {
    var r = new Float64Array(16);
    var im = 1.0 / _MJS_v3lengthLocal(axis);
    var x = axis[0] * im;
    var y = axis[1] * im;
    var z = axis[2] * im;
    var c = Math.cos(angle);
    var c1 = 1 - c;
    var s = Math.sin(angle);
    var xs = x * s;
    var ys = y * s;
    var zs = z * s;
    var xyc1 = x * y * c1;
    var xzc1 = x * z * c1;
    var yzc1 = y * z * c1;
    var t11 = x * x * c1 + c;
    var t21 = xyc1 + zs;
    var t31 = xzc1 - ys;
    var t12 = xyc1 - zs;
    var t22 = y * y * c1 + c;
    var t32 = yzc1 + xs;
    var t13 = xzc1 + ys;
    var t23 = yzc1 - xs;
    var t33 = z * z * c1 + c;
    var m11 = m[0], m21 = m[1], m31 = m[2], m41 = m[3];
    var m12 = m[4], m22 = m[5], m32 = m[6], m42 = m[7];
    var m13 = m[8], m23 = m[9], m33 = m[10], m43 = m[11];
    var m14 = m[12], m24 = m[13], m34 = m[14], m44 = m[15];

    r[0] = m11 * t11 + m12 * t21 + m13 * t31;
    r[1] = m21 * t11 + m22 * t21 + m23 * t31;
    r[2] = m31 * t11 + m32 * t21 + m33 * t31;
    r[3] = m41 * t11 + m42 * t21 + m43 * t31;
    r[4] = m11 * t12 + m12 * t22 + m13 * t32;
    r[5] = m21 * t12 + m22 * t22 + m23 * t32;
    r[6] = m31 * t12 + m32 * t22 + m33 * t32;
    r[7] = m41 * t12 + m42 * t22 + m43 * t32;
    r[8] = m11 * t13 + m12 * t23 + m13 * t33;
    r[9] = m21 * t13 + m22 * t23 + m23 * t33;
    r[10] = m31 * t13 + m32 * t23 + m33 * t33;
    r[11] = m41 * t13 + m42 * t23 + m43 * t33;
    r[12] = m14,
    r[13] = m24;
    r[14] = m34;
    r[15] = m44;

    return r;
});

function _MJS_m4x4makeScale3Local(x, y, z) {
    var r = new Float64Array(16);

    r[0] = x;
    r[1] = 0;
    r[2] = 0;
    r[3] = 0;
    r[4] = 0;
    r[5] = y;
    r[6] = 0;
    r[7] = 0;
    r[8] = 0;
    r[9] = 0;
    r[10] = z;
    r[11] = 0;
    r[12] = 0;
    r[13] = 0;
    r[14] = 0;
    r[15] = 1;

    return r;
}
var _MJS_m4x4makeScale3 = F3(_MJS_m4x4makeScale3Local);

var _MJS_m4x4makeScale = function(v) {
    return _MJS_m4x4makeScale3Local(v[0], v[1], v[2]);
};

var _MJS_m4x4scale3 = F4(function(x, y, z, m) {
    var r = new Float64Array(16);

    r[0] = m[0] * x;
    r[1] = m[1] * x;
    r[2] = m[2] * x;
    r[3] = m[3] * x;
    r[4] = m[4] * y;
    r[5] = m[5] * y;
    r[6] = m[6] * y;
    r[7] = m[7] * y;
    r[8] = m[8] * z;
    r[9] = m[9] * z;
    r[10] = m[10] * z;
    r[11] = m[11] * z;
    r[12] = m[12];
    r[13] = m[13];
    r[14] = m[14];
    r[15] = m[15];

    return r;
});

var _MJS_m4x4scale = F2(function(v, m) {
    var r = new Float64Array(16);
    var x = v[0];
    var y = v[1];
    var z = v[2];

    r[0] = m[0] * x;
    r[1] = m[1] * x;
    r[2] = m[2] * x;
    r[3] = m[3] * x;
    r[4] = m[4] * y;
    r[5] = m[5] * y;
    r[6] = m[6] * y;
    r[7] = m[7] * y;
    r[8] = m[8] * z;
    r[9] = m[9] * z;
    r[10] = m[10] * z;
    r[11] = m[11] * z;
    r[12] = m[12];
    r[13] = m[13];
    r[14] = m[14];
    r[15] = m[15];

    return r;
});

function _MJS_m4x4makeTranslate3Local(x, y, z) {
    var r = new Float64Array(16);

    r[0] = 1;
    r[1] = 0;
    r[2] = 0;
    r[3] = 0;
    r[4] = 0;
    r[5] = 1;
    r[6] = 0;
    r[7] = 0;
    r[8] = 0;
    r[9] = 0;
    r[10] = 1;
    r[11] = 0;
    r[12] = x;
    r[13] = y;
    r[14] = z;
    r[15] = 1;

    return r;
}
var _MJS_m4x4makeTranslate3 = F3(_MJS_m4x4makeTranslate3Local);

var _MJS_m4x4makeTranslate = function(v) {
    return _MJS_m4x4makeTranslate3Local(v[0], v[1], v[2]);
};

var _MJS_m4x4translate3 = F4(function(x, y, z, m) {
    var r = new Float64Array(16);
    var m11 = m[0];
    var m21 = m[1];
    var m31 = m[2];
    var m41 = m[3];
    var m12 = m[4];
    var m22 = m[5];
    var m32 = m[6];
    var m42 = m[7];
    var m13 = m[8];
    var m23 = m[9];
    var m33 = m[10];
    var m43 = m[11];

    r[0] = m11;
    r[1] = m21;
    r[2] = m31;
    r[3] = m41;
    r[4] = m12;
    r[5] = m22;
    r[6] = m32;
    r[7] = m42;
    r[8] = m13;
    r[9] = m23;
    r[10] = m33;
    r[11] = m43;
    r[12] = m11 * x + m12 * y + m13 * z + m[12];
    r[13] = m21 * x + m22 * y + m23 * z + m[13];
    r[14] = m31 * x + m32 * y + m33 * z + m[14];
    r[15] = m41 * x + m42 * y + m43 * z + m[15];

    return r;
});

var _MJS_m4x4translate = F2(function(v, m) {
    var r = new Float64Array(16);
    var x = v[0];
    var y = v[1];
    var z = v[2];
    var m11 = m[0];
    var m21 = m[1];
    var m31 = m[2];
    var m41 = m[3];
    var m12 = m[4];
    var m22 = m[5];
    var m32 = m[6];
    var m42 = m[7];
    var m13 = m[8];
    var m23 = m[9];
    var m33 = m[10];
    var m43 = m[11];

    r[0] = m11;
    r[1] = m21;
    r[2] = m31;
    r[3] = m41;
    r[4] = m12;
    r[5] = m22;
    r[6] = m32;
    r[7] = m42;
    r[8] = m13;
    r[9] = m23;
    r[10] = m33;
    r[11] = m43;
    r[12] = m11 * x + m12 * y + m13 * z + m[12];
    r[13] = m21 * x + m22 * y + m23 * z + m[13];
    r[14] = m31 * x + m32 * y + m33 * z + m[14];
    r[15] = m41 * x + m42 * y + m43 * z + m[15];

    return r;
});

var _MJS_m4x4makeLookAt = F3(function(eye, center, up) {
    var z = _MJS_v3directionLocal(eye, center, _MJS_v3temp1Local);
    var x = _MJS_v3normalizeLocal(_MJS_v3crossLocal(up, z, _MJS_v3temp2Local), _MJS_v3temp2Local);
    var y = _MJS_v3normalizeLocal(_MJS_v3crossLocal(z, x, _MJS_v3temp3Local), _MJS_v3temp3Local);
    var tm1 = _MJS_m4x4temp1Local;
    var tm2 = _MJS_m4x4temp2Local;

    tm1[0] = x[0];
    tm1[1] = y[0];
    tm1[2] = z[0];
    tm1[3] = 0;
    tm1[4] = x[1];
    tm1[5] = y[1];
    tm1[6] = z[1];
    tm1[7] = 0;
    tm1[8] = x[2];
    tm1[9] = y[2];
    tm1[10] = z[2];
    tm1[11] = 0;
    tm1[12] = 0;
    tm1[13] = 0;
    tm1[14] = 0;
    tm1[15] = 1;

    tm2[0] = 1; tm2[1] = 0; tm2[2] = 0; tm2[3] = 0;
    tm2[4] = 0; tm2[5] = 1; tm2[6] = 0; tm2[7] = 0;
    tm2[8] = 0; tm2[9] = 0; tm2[10] = 1; tm2[11] = 0;
    tm2[12] = -eye[0]; tm2[13] = -eye[1]; tm2[14] = -eye[2]; tm2[15] = 1;

    return _MJS_m4x4mulLocal(tm1, tm2);
});


function _MJS_m4x4transposeLocal(m) {
    var r = new Float64Array(16);

    r[0] = m[0]; r[1] = m[4]; r[2] = m[8]; r[3] = m[12];
    r[4] = m[1]; r[5] = m[5]; r[6] = m[9]; r[7] = m[13];
    r[8] = m[2]; r[9] = m[6]; r[10] = m[10]; r[11] = m[14];
    r[12] = m[3]; r[13] = m[7]; r[14] = m[11]; r[15] = m[15];

    return r;
}
var _MJS_m4x4transpose = _MJS_m4x4transposeLocal;

var _MJS_m4x4makeBasis = F3(function(vx, vy, vz) {
    var r = new Float64Array(16);

    r[0] = vx[0];
    r[1] = vx[1];
    r[2] = vx[2];
    r[3] = 0;
    r[4] = vy[0];
    r[5] = vy[1];
    r[6] = vy[2];
    r[7] = 0;
    r[8] = vz[0];
    r[9] = vz[1];
    r[10] = vz[2];
    r[11] = 0;
    r[12] = 0;
    r[13] = 0;
    r[14] = 0;
    r[15] = 1;

    return r;
});



// SEND REQUEST

var _Http_toTask = F3(function(router, toTask, request)
{
	return _Scheduler_binding(function(callback)
	{
		function done(response) {
			callback(toTask(request.expect.a(response)));
		}

		var xhr = new XMLHttpRequest();
		xhr.addEventListener('error', function() { done($elm$http$Http$NetworkError_); });
		xhr.addEventListener('timeout', function() { done($elm$http$Http$Timeout_); });
		xhr.addEventListener('load', function() { done(_Http_toResponse(request.expect.b, xhr)); });
		$elm$core$Maybe$isJust(request.tracker) && _Http_track(router, xhr, request.tracker.a);

		try {
			xhr.open(request.method, request.url, true);
		} catch (e) {
			return done($elm$http$Http$BadUrl_(request.url));
		}

		_Http_configureRequest(xhr, request);

		request.body.a && xhr.setRequestHeader('Content-Type', request.body.a);
		xhr.send(request.body.b);

		return function() { xhr.c = true; xhr.abort(); };
	});
});


// CONFIGURE

function _Http_configureRequest(xhr, request)
{
	for (var headers = request.headers; headers.b; headers = headers.b) // WHILE_CONS
	{
		xhr.setRequestHeader(headers.a.a, headers.a.b);
	}
	xhr.timeout = request.timeout.a || 0;
	xhr.responseType = request.expect.d;
	xhr.withCredentials = request.allowCookiesFromOtherDomains;
}


// RESPONSES

function _Http_toResponse(toBody, xhr)
{
	return A2(
		200 <= xhr.status && xhr.status < 300 ? $elm$http$Http$GoodStatus_ : $elm$http$Http$BadStatus_,
		_Http_toMetadata(xhr),
		toBody(xhr.response)
	);
}


// METADATA

function _Http_toMetadata(xhr)
{
	return {
		url: xhr.responseURL,
		statusCode: xhr.status,
		statusText: xhr.statusText,
		headers: _Http_parseHeaders(xhr.getAllResponseHeaders())
	};
}


// HEADERS

function _Http_parseHeaders(rawHeaders)
{
	if (!rawHeaders)
	{
		return $elm$core$Dict$empty;
	}

	var headers = $elm$core$Dict$empty;
	var headerPairs = rawHeaders.split('\r\n');
	for (var i = headerPairs.length; i--; )
	{
		var headerPair = headerPairs[i];
		var index = headerPair.indexOf(': ');
		if (index > 0)
		{
			var key = headerPair.substring(0, index);
			var value = headerPair.substring(index + 2);

			headers = A3($elm$core$Dict$update, key, function(oldValue) {
				return $elm$core$Maybe$Just($elm$core$Maybe$isJust(oldValue)
					? value + ', ' + oldValue.a
					: value
				);
			}, headers);
		}
	}
	return headers;
}


// EXPECT

var _Http_expect = F3(function(type, toBody, toValue)
{
	return {
		$: 0,
		d: type,
		b: toBody,
		a: toValue
	};
});

var _Http_mapExpect = F2(function(func, expect)
{
	return {
		$: 0,
		d: expect.d,
		b: expect.b,
		a: function(x) { return func(expect.a(x)); }
	};
});

function _Http_toDataView(arrayBuffer)
{
	return new DataView(arrayBuffer);
}


// BODY and PARTS

var _Http_emptyBody = { $: 0 };
var _Http_pair = F2(function(a, b) { return { $: 0, a: a, b: b }; });

function _Http_toFormData(parts)
{
	for (var formData = new FormData(); parts.b; parts = parts.b) // WHILE_CONS
	{
		var part = parts.a;
		formData.append(part.a, part.b);
	}
	return formData;
}

var _Http_bytesToBlob = F2(function(mime, bytes)
{
	return new Blob([bytes], { type: mime });
});


// PROGRESS

function _Http_track(router, xhr, tracker)
{
	// TODO check out lengthComputable on loadstart event

	xhr.upload.addEventListener('progress', function(event) {
		if (xhr.c) { return; }
		_Scheduler_rawSpawn(A2($elm$core$Platform$sendToSelf, router, _Utils_Tuple2(tracker, $elm$http$Http$Sending({
			sent: event.loaded,
			size: event.total
		}))));
	});
	xhr.addEventListener('progress', function(event) {
		if (xhr.c) { return; }
		_Scheduler_rawSpawn(A2($elm$core$Platform$sendToSelf, router, _Utils_Tuple2(tracker, $elm$http$Http$Receiving({
			received: event.loaded,
			size: event.lengthComputable ? $elm$core$Maybe$Just(event.total) : $elm$core$Maybe$Nothing
		}))));
	});
}var $elm$core$Basics$EQ = {$: 'EQ'};
var $elm$core$Basics$GT = {$: 'GT'};
var $elm$core$Basics$LT = {$: 'LT'};
var $elm$core$List$cons = _List_cons;
var $elm$core$Dict$foldr = F3(
	function (func, acc, t) {
		foldr:
		while (true) {
			if (t.$ === 'RBEmpty_elm_builtin') {
				return acc;
			} else {
				var key = t.b;
				var value = t.c;
				var left = t.d;
				var right = t.e;
				var $temp$func = func,
					$temp$acc = A3(
					func,
					key,
					value,
					A3($elm$core$Dict$foldr, func, acc, right)),
					$temp$t = left;
				func = $temp$func;
				acc = $temp$acc;
				t = $temp$t;
				continue foldr;
			}
		}
	});
var $elm$core$Dict$toList = function (dict) {
	return A3(
		$elm$core$Dict$foldr,
		F3(
			function (key, value, list) {
				return A2(
					$elm$core$List$cons,
					_Utils_Tuple2(key, value),
					list);
			}),
		_List_Nil,
		dict);
};
var $elm$core$Dict$keys = function (dict) {
	return A3(
		$elm$core$Dict$foldr,
		F3(
			function (key, value, keyList) {
				return A2($elm$core$List$cons, key, keyList);
			}),
		_List_Nil,
		dict);
};
var $elm$core$Set$toList = function (_v0) {
	var dict = _v0.a;
	return $elm$core$Dict$keys(dict);
};
var $elm$core$Elm$JsArray$foldr = _JsArray_foldr;
var $elm$core$Array$foldr = F3(
	function (func, baseCase, _v0) {
		var tree = _v0.c;
		var tail = _v0.d;
		var helper = F2(
			function (node, acc) {
				if (node.$ === 'SubTree') {
					var subTree = node.a;
					return A3($elm$core$Elm$JsArray$foldr, helper, acc, subTree);
				} else {
					var values = node.a;
					return A3($elm$core$Elm$JsArray$foldr, func, acc, values);
				}
			});
		return A3(
			$elm$core$Elm$JsArray$foldr,
			helper,
			A3($elm$core$Elm$JsArray$foldr, func, baseCase, tail),
			tree);
	});
var $elm$core$Array$toList = function (array) {
	return A3($elm$core$Array$foldr, $elm$core$List$cons, _List_Nil, array);
};
var $elm$core$Result$Err = function (a) {
	return {$: 'Err', a: a};
};
var $elm$json$Json$Decode$Failure = F2(
	function (a, b) {
		return {$: 'Failure', a: a, b: b};
	});
var $elm$json$Json$Decode$Field = F2(
	function (a, b) {
		return {$: 'Field', a: a, b: b};
	});
var $elm$json$Json$Decode$Index = F2(
	function (a, b) {
		return {$: 'Index', a: a, b: b};
	});
var $elm$core$Result$Ok = function (a) {
	return {$: 'Ok', a: a};
};
var $elm$json$Json$Decode$OneOf = function (a) {
	return {$: 'OneOf', a: a};
};
var $elm$core$Basics$False = {$: 'False'};
var $elm$core$Basics$add = _Basics_add;
var $elm$core$Maybe$Just = function (a) {
	return {$: 'Just', a: a};
};
var $elm$core$Maybe$Nothing = {$: 'Nothing'};
var $elm$core$String$all = _String_all;
var $elm$core$Basics$and = _Basics_and;
var $elm$core$Basics$append = _Utils_append;
var $elm$json$Json$Encode$encode = _Json_encode;
var $elm$core$String$fromInt = _String_fromNumber;
var $elm$core$String$join = F2(
	function (sep, chunks) {
		return A2(
			_String_join,
			sep,
			_List_toArray(chunks));
	});
var $elm$core$String$split = F2(
	function (sep, string) {
		return _List_fromArray(
			A2(_String_split, sep, string));
	});
var $elm$json$Json$Decode$indent = function (str) {
	return A2(
		$elm$core$String$join,
		'\n    ',
		A2($elm$core$String$split, '\n', str));
};
var $elm$core$List$foldl = F3(
	function (func, acc, list) {
		foldl:
		while (true) {
			if (!list.b) {
				return acc;
			} else {
				var x = list.a;
				var xs = list.b;
				var $temp$func = func,
					$temp$acc = A2(func, x, acc),
					$temp$list = xs;
				func = $temp$func;
				acc = $temp$acc;
				list = $temp$list;
				continue foldl;
			}
		}
	});
var $elm$core$List$length = function (xs) {
	return A3(
		$elm$core$List$foldl,
		F2(
			function (_v0, i) {
				return i + 1;
			}),
		0,
		xs);
};
var $elm$core$List$map2 = _List_map2;
var $elm$core$Basics$le = _Utils_le;
var $elm$core$Basics$sub = _Basics_sub;
var $elm$core$List$rangeHelp = F3(
	function (lo, hi, list) {
		rangeHelp:
		while (true) {
			if (_Utils_cmp(lo, hi) < 1) {
				var $temp$lo = lo,
					$temp$hi = hi - 1,
					$temp$list = A2($elm$core$List$cons, hi, list);
				lo = $temp$lo;
				hi = $temp$hi;
				list = $temp$list;
				continue rangeHelp;
			} else {
				return list;
			}
		}
	});
var $elm$core$List$range = F2(
	function (lo, hi) {
		return A3($elm$core$List$rangeHelp, lo, hi, _List_Nil);
	});
var $elm$core$List$indexedMap = F2(
	function (f, xs) {
		return A3(
			$elm$core$List$map2,
			f,
			A2(
				$elm$core$List$range,
				0,
				$elm$core$List$length(xs) - 1),
			xs);
	});
var $elm$core$Char$toCode = _Char_toCode;
var $elm$core$Char$isLower = function (_char) {
	var code = $elm$core$Char$toCode(_char);
	return (97 <= code) && (code <= 122);
};
var $elm$core$Char$isUpper = function (_char) {
	var code = $elm$core$Char$toCode(_char);
	return (code <= 90) && (65 <= code);
};
var $elm$core$Basics$or = _Basics_or;
var $elm$core$Char$isAlpha = function (_char) {
	return $elm$core$Char$isLower(_char) || $elm$core$Char$isUpper(_char);
};
var $elm$core$Char$isDigit = function (_char) {
	var code = $elm$core$Char$toCode(_char);
	return (code <= 57) && (48 <= code);
};
var $elm$core$Char$isAlphaNum = function (_char) {
	return $elm$core$Char$isLower(_char) || ($elm$core$Char$isUpper(_char) || $elm$core$Char$isDigit(_char));
};
var $elm$core$List$reverse = function (list) {
	return A3($elm$core$List$foldl, $elm$core$List$cons, _List_Nil, list);
};
var $elm$core$String$uncons = _String_uncons;
var $elm$json$Json$Decode$errorOneOf = F2(
	function (i, error) {
		return '\n\n(' + ($elm$core$String$fromInt(i + 1) + (') ' + $elm$json$Json$Decode$indent(
			$elm$json$Json$Decode$errorToString(error))));
	});
var $elm$json$Json$Decode$errorToString = function (error) {
	return A2($elm$json$Json$Decode$errorToStringHelp, error, _List_Nil);
};
var $elm$json$Json$Decode$errorToStringHelp = F2(
	function (error, context) {
		errorToStringHelp:
		while (true) {
			switch (error.$) {
				case 'Field':
					var f = error.a;
					var err = error.b;
					var isSimple = function () {
						var _v1 = $elm$core$String$uncons(f);
						if (_v1.$ === 'Nothing') {
							return false;
						} else {
							var _v2 = _v1.a;
							var _char = _v2.a;
							var rest = _v2.b;
							return $elm$core$Char$isAlpha(_char) && A2($elm$core$String$all, $elm$core$Char$isAlphaNum, rest);
						}
					}();
					var fieldName = isSimple ? ('.' + f) : ('[\'' + (f + '\']'));
					var $temp$error = err,
						$temp$context = A2($elm$core$List$cons, fieldName, context);
					error = $temp$error;
					context = $temp$context;
					continue errorToStringHelp;
				case 'Index':
					var i = error.a;
					var err = error.b;
					var indexName = '[' + ($elm$core$String$fromInt(i) + ']');
					var $temp$error = err,
						$temp$context = A2($elm$core$List$cons, indexName, context);
					error = $temp$error;
					context = $temp$context;
					continue errorToStringHelp;
				case 'OneOf':
					var errors = error.a;
					if (!errors.b) {
						return 'Ran into a Json.Decode.oneOf with no possibilities' + function () {
							if (!context.b) {
								return '!';
							} else {
								return ' at json' + A2(
									$elm$core$String$join,
									'',
									$elm$core$List$reverse(context));
							}
						}();
					} else {
						if (!errors.b.b) {
							var err = errors.a;
							var $temp$error = err,
								$temp$context = context;
							error = $temp$error;
							context = $temp$context;
							continue errorToStringHelp;
						} else {
							var starter = function () {
								if (!context.b) {
									return 'Json.Decode.oneOf';
								} else {
									return 'The Json.Decode.oneOf at json' + A2(
										$elm$core$String$join,
										'',
										$elm$core$List$reverse(context));
								}
							}();
							var introduction = starter + (' failed in the following ' + ($elm$core$String$fromInt(
								$elm$core$List$length(errors)) + ' ways:'));
							return A2(
								$elm$core$String$join,
								'\n\n',
								A2(
									$elm$core$List$cons,
									introduction,
									A2($elm$core$List$indexedMap, $elm$json$Json$Decode$errorOneOf, errors)));
						}
					}
				default:
					var msg = error.a;
					var json = error.b;
					var introduction = function () {
						if (!context.b) {
							return 'Problem with the given value:\n\n';
						} else {
							return 'Problem with the value at json' + (A2(
								$elm$core$String$join,
								'',
								$elm$core$List$reverse(context)) + ':\n\n    ');
						}
					}();
					return introduction + ($elm$json$Json$Decode$indent(
						A2($elm$json$Json$Encode$encode, 4, json)) + ('\n\n' + msg));
			}
		}
	});
var $elm$core$Array$branchFactor = 32;
var $elm$core$Array$Array_elm_builtin = F4(
	function (a, b, c, d) {
		return {$: 'Array_elm_builtin', a: a, b: b, c: c, d: d};
	});
var $elm$core$Elm$JsArray$empty = _JsArray_empty;
var $elm$core$Basics$ceiling = _Basics_ceiling;
var $elm$core$Basics$fdiv = _Basics_fdiv;
var $elm$core$Basics$logBase = F2(
	function (base, number) {
		return _Basics_log(number) / _Basics_log(base);
	});
var $elm$core$Basics$toFloat = _Basics_toFloat;
var $elm$core$Array$shiftStep = $elm$core$Basics$ceiling(
	A2($elm$core$Basics$logBase, 2, $elm$core$Array$branchFactor));
var $elm$core$Array$empty = A4($elm$core$Array$Array_elm_builtin, 0, $elm$core$Array$shiftStep, $elm$core$Elm$JsArray$empty, $elm$core$Elm$JsArray$empty);
var $elm$core$Elm$JsArray$initialize = _JsArray_initialize;
var $elm$core$Array$Leaf = function (a) {
	return {$: 'Leaf', a: a};
};
var $elm$core$Basics$apL = F2(
	function (f, x) {
		return f(x);
	});
var $elm$core$Basics$apR = F2(
	function (x, f) {
		return f(x);
	});
var $elm$core$Basics$eq = _Utils_equal;
var $elm$core$Basics$floor = _Basics_floor;
var $elm$core$Elm$JsArray$length = _JsArray_length;
var $elm$core$Basics$gt = _Utils_gt;
var $elm$core$Basics$max = F2(
	function (x, y) {
		return (_Utils_cmp(x, y) > 0) ? x : y;
	});
var $elm$core$Basics$mul = _Basics_mul;
var $elm$core$Array$SubTree = function (a) {
	return {$: 'SubTree', a: a};
};
var $elm$core$Elm$JsArray$initializeFromList = _JsArray_initializeFromList;
var $elm$core$Array$compressNodes = F2(
	function (nodes, acc) {
		compressNodes:
		while (true) {
			var _v0 = A2($elm$core$Elm$JsArray$initializeFromList, $elm$core$Array$branchFactor, nodes);
			var node = _v0.a;
			var remainingNodes = _v0.b;
			var newAcc = A2(
				$elm$core$List$cons,
				$elm$core$Array$SubTree(node),
				acc);
			if (!remainingNodes.b) {
				return $elm$core$List$reverse(newAcc);
			} else {
				var $temp$nodes = remainingNodes,
					$temp$acc = newAcc;
				nodes = $temp$nodes;
				acc = $temp$acc;
				continue compressNodes;
			}
		}
	});
var $elm$core$Tuple$first = function (_v0) {
	var x = _v0.a;
	return x;
};
var $elm$core$Array$treeFromBuilder = F2(
	function (nodeList, nodeListSize) {
		treeFromBuilder:
		while (true) {
			var newNodeSize = $elm$core$Basics$ceiling(nodeListSize / $elm$core$Array$branchFactor);
			if (newNodeSize === 1) {
				return A2($elm$core$Elm$JsArray$initializeFromList, $elm$core$Array$branchFactor, nodeList).a;
			} else {
				var $temp$nodeList = A2($elm$core$Array$compressNodes, nodeList, _List_Nil),
					$temp$nodeListSize = newNodeSize;
				nodeList = $temp$nodeList;
				nodeListSize = $temp$nodeListSize;
				continue treeFromBuilder;
			}
		}
	});
var $elm$core$Array$builderToArray = F2(
	function (reverseNodeList, builder) {
		if (!builder.nodeListSize) {
			return A4(
				$elm$core$Array$Array_elm_builtin,
				$elm$core$Elm$JsArray$length(builder.tail),
				$elm$core$Array$shiftStep,
				$elm$core$Elm$JsArray$empty,
				builder.tail);
		} else {
			var treeLen = builder.nodeListSize * $elm$core$Array$branchFactor;
			var depth = $elm$core$Basics$floor(
				A2($elm$core$Basics$logBase, $elm$core$Array$branchFactor, treeLen - 1));
			var correctNodeList = reverseNodeList ? $elm$core$List$reverse(builder.nodeList) : builder.nodeList;
			var tree = A2($elm$core$Array$treeFromBuilder, correctNodeList, builder.nodeListSize);
			return A4(
				$elm$core$Array$Array_elm_builtin,
				$elm$core$Elm$JsArray$length(builder.tail) + treeLen,
				A2($elm$core$Basics$max, 5, depth * $elm$core$Array$shiftStep),
				tree,
				builder.tail);
		}
	});
var $elm$core$Basics$idiv = _Basics_idiv;
var $elm$core$Basics$lt = _Utils_lt;
var $elm$core$Array$initializeHelp = F5(
	function (fn, fromIndex, len, nodeList, tail) {
		initializeHelp:
		while (true) {
			if (fromIndex < 0) {
				return A2(
					$elm$core$Array$builderToArray,
					false,
					{nodeList: nodeList, nodeListSize: (len / $elm$core$Array$branchFactor) | 0, tail: tail});
			} else {
				var leaf = $elm$core$Array$Leaf(
					A3($elm$core$Elm$JsArray$initialize, $elm$core$Array$branchFactor, fromIndex, fn));
				var $temp$fn = fn,
					$temp$fromIndex = fromIndex - $elm$core$Array$branchFactor,
					$temp$len = len,
					$temp$nodeList = A2($elm$core$List$cons, leaf, nodeList),
					$temp$tail = tail;
				fn = $temp$fn;
				fromIndex = $temp$fromIndex;
				len = $temp$len;
				nodeList = $temp$nodeList;
				tail = $temp$tail;
				continue initializeHelp;
			}
		}
	});
var $elm$core$Basics$remainderBy = _Basics_remainderBy;
var $elm$core$Array$initialize = F2(
	function (len, fn) {
		if (len <= 0) {
			return $elm$core$Array$empty;
		} else {
			var tailLen = len % $elm$core$Array$branchFactor;
			var tail = A3($elm$core$Elm$JsArray$initialize, tailLen, len - tailLen, fn);
			var initialFromIndex = (len - tailLen) - $elm$core$Array$branchFactor;
			return A5($elm$core$Array$initializeHelp, fn, initialFromIndex, len, _List_Nil, tail);
		}
	});
var $elm$core$Basics$True = {$: 'True'};
var $elm$core$Result$isOk = function (result) {
	if (result.$ === 'Ok') {
		return true;
	} else {
		return false;
	}
};
var $elm$json$Json$Decode$map = _Json_map1;
var $elm$json$Json$Decode$map2 = _Json_map2;
var $elm$json$Json$Decode$succeed = _Json_succeed;
var $elm$virtual_dom$VirtualDom$toHandlerInt = function (handler) {
	switch (handler.$) {
		case 'Normal':
			return 0;
		case 'MayStopPropagation':
			return 1;
		case 'MayPreventDefault':
			return 2;
		default:
			return 3;
	}
};
var $elm$browser$Browser$External = function (a) {
	return {$: 'External', a: a};
};
var $elm$browser$Browser$Internal = function (a) {
	return {$: 'Internal', a: a};
};
var $elm$core$Basics$identity = function (x) {
	return x;
};
var $elm$browser$Browser$Dom$NotFound = function (a) {
	return {$: 'NotFound', a: a};
};
var $elm$url$Url$Http = {$: 'Http'};
var $elm$url$Url$Https = {$: 'Https'};
var $elm$url$Url$Url = F6(
	function (protocol, host, port_, path, query, fragment) {
		return {fragment: fragment, host: host, path: path, port_: port_, protocol: protocol, query: query};
	});
var $elm$core$String$contains = _String_contains;
var $elm$core$String$length = _String_length;
var $elm$core$String$slice = _String_slice;
var $elm$core$String$dropLeft = F2(
	function (n, string) {
		return (n < 1) ? string : A3(
			$elm$core$String$slice,
			n,
			$elm$core$String$length(string),
			string);
	});
var $elm$core$String$indexes = _String_indexes;
var $elm$core$String$isEmpty = function (string) {
	return string === '';
};
var $elm$core$String$left = F2(
	function (n, string) {
		return (n < 1) ? '' : A3($elm$core$String$slice, 0, n, string);
	});
var $elm$core$String$toInt = _String_toInt;
var $elm$url$Url$chompBeforePath = F5(
	function (protocol, path, params, frag, str) {
		if ($elm$core$String$isEmpty(str) || A2($elm$core$String$contains, '@', str)) {
			return $elm$core$Maybe$Nothing;
		} else {
			var _v0 = A2($elm$core$String$indexes, ':', str);
			if (!_v0.b) {
				return $elm$core$Maybe$Just(
					A6($elm$url$Url$Url, protocol, str, $elm$core$Maybe$Nothing, path, params, frag));
			} else {
				if (!_v0.b.b) {
					var i = _v0.a;
					var _v1 = $elm$core$String$toInt(
						A2($elm$core$String$dropLeft, i + 1, str));
					if (_v1.$ === 'Nothing') {
						return $elm$core$Maybe$Nothing;
					} else {
						var port_ = _v1;
						return $elm$core$Maybe$Just(
							A6(
								$elm$url$Url$Url,
								protocol,
								A2($elm$core$String$left, i, str),
								port_,
								path,
								params,
								frag));
					}
				} else {
					return $elm$core$Maybe$Nothing;
				}
			}
		}
	});
var $elm$url$Url$chompBeforeQuery = F4(
	function (protocol, params, frag, str) {
		if ($elm$core$String$isEmpty(str)) {
			return $elm$core$Maybe$Nothing;
		} else {
			var _v0 = A2($elm$core$String$indexes, '/', str);
			if (!_v0.b) {
				return A5($elm$url$Url$chompBeforePath, protocol, '/', params, frag, str);
			} else {
				var i = _v0.a;
				return A5(
					$elm$url$Url$chompBeforePath,
					protocol,
					A2($elm$core$String$dropLeft, i, str),
					params,
					frag,
					A2($elm$core$String$left, i, str));
			}
		}
	});
var $elm$url$Url$chompBeforeFragment = F3(
	function (protocol, frag, str) {
		if ($elm$core$String$isEmpty(str)) {
			return $elm$core$Maybe$Nothing;
		} else {
			var _v0 = A2($elm$core$String$indexes, '?', str);
			if (!_v0.b) {
				return A4($elm$url$Url$chompBeforeQuery, protocol, $elm$core$Maybe$Nothing, frag, str);
			} else {
				var i = _v0.a;
				return A4(
					$elm$url$Url$chompBeforeQuery,
					protocol,
					$elm$core$Maybe$Just(
						A2($elm$core$String$dropLeft, i + 1, str)),
					frag,
					A2($elm$core$String$left, i, str));
			}
		}
	});
var $elm$url$Url$chompAfterProtocol = F2(
	function (protocol, str) {
		if ($elm$core$String$isEmpty(str)) {
			return $elm$core$Maybe$Nothing;
		} else {
			var _v0 = A2($elm$core$String$indexes, '#', str);
			if (!_v0.b) {
				return A3($elm$url$Url$chompBeforeFragment, protocol, $elm$core$Maybe$Nothing, str);
			} else {
				var i = _v0.a;
				return A3(
					$elm$url$Url$chompBeforeFragment,
					protocol,
					$elm$core$Maybe$Just(
						A2($elm$core$String$dropLeft, i + 1, str)),
					A2($elm$core$String$left, i, str));
			}
		}
	});
var $elm$core$String$startsWith = _String_startsWith;
var $elm$url$Url$fromString = function (str) {
	return A2($elm$core$String$startsWith, 'http://', str) ? A2(
		$elm$url$Url$chompAfterProtocol,
		$elm$url$Url$Http,
		A2($elm$core$String$dropLeft, 7, str)) : (A2($elm$core$String$startsWith, 'https://', str) ? A2(
		$elm$url$Url$chompAfterProtocol,
		$elm$url$Url$Https,
		A2($elm$core$String$dropLeft, 8, str)) : $elm$core$Maybe$Nothing);
};
var $elm$core$Basics$never = function (_v0) {
	never:
	while (true) {
		var nvr = _v0.a;
		var $temp$_v0 = nvr;
		_v0 = $temp$_v0;
		continue never;
	}
};
var $elm$core$Task$Perform = function (a) {
	return {$: 'Perform', a: a};
};
var $elm$core$Task$succeed = _Scheduler_succeed;
var $elm$core$Task$init = $elm$core$Task$succeed(_Utils_Tuple0);
var $elm$core$List$foldrHelper = F4(
	function (fn, acc, ctr, ls) {
		if (!ls.b) {
			return acc;
		} else {
			var a = ls.a;
			var r1 = ls.b;
			if (!r1.b) {
				return A2(fn, a, acc);
			} else {
				var b = r1.a;
				var r2 = r1.b;
				if (!r2.b) {
					return A2(
						fn,
						a,
						A2(fn, b, acc));
				} else {
					var c = r2.a;
					var r3 = r2.b;
					if (!r3.b) {
						return A2(
							fn,
							a,
							A2(
								fn,
								b,
								A2(fn, c, acc)));
					} else {
						var d = r3.a;
						var r4 = r3.b;
						var res = (ctr > 500) ? A3(
							$elm$core$List$foldl,
							fn,
							acc,
							$elm$core$List$reverse(r4)) : A4($elm$core$List$foldrHelper, fn, acc, ctr + 1, r4);
						return A2(
							fn,
							a,
							A2(
								fn,
								b,
								A2(
									fn,
									c,
									A2(fn, d, res))));
					}
				}
			}
		}
	});
var $elm$core$List$foldr = F3(
	function (fn, acc, ls) {
		return A4($elm$core$List$foldrHelper, fn, acc, 0, ls);
	});
var $elm$core$List$map = F2(
	function (f, xs) {
		return A3(
			$elm$core$List$foldr,
			F2(
				function (x, acc) {
					return A2(
						$elm$core$List$cons,
						f(x),
						acc);
				}),
			_List_Nil,
			xs);
	});
var $elm$core$Task$andThen = _Scheduler_andThen;
var $elm$core$Task$map = F2(
	function (func, taskA) {
		return A2(
			$elm$core$Task$andThen,
			function (a) {
				return $elm$core$Task$succeed(
					func(a));
			},
			taskA);
	});
var $elm$core$Task$map2 = F3(
	function (func, taskA, taskB) {
		return A2(
			$elm$core$Task$andThen,
			function (a) {
				return A2(
					$elm$core$Task$andThen,
					function (b) {
						return $elm$core$Task$succeed(
							A2(func, a, b));
					},
					taskB);
			},
			taskA);
	});
var $elm$core$Task$sequence = function (tasks) {
	return A3(
		$elm$core$List$foldr,
		$elm$core$Task$map2($elm$core$List$cons),
		$elm$core$Task$succeed(_List_Nil),
		tasks);
};
var $elm$core$Platform$sendToApp = _Platform_sendToApp;
var $elm$core$Task$spawnCmd = F2(
	function (router, _v0) {
		var task = _v0.a;
		return _Scheduler_spawn(
			A2(
				$elm$core$Task$andThen,
				$elm$core$Platform$sendToApp(router),
				task));
	});
var $elm$core$Task$onEffects = F3(
	function (router, commands, state) {
		return A2(
			$elm$core$Task$map,
			function (_v0) {
				return _Utils_Tuple0;
			},
			$elm$core$Task$sequence(
				A2(
					$elm$core$List$map,
					$elm$core$Task$spawnCmd(router),
					commands)));
	});
var $elm$core$Task$onSelfMsg = F3(
	function (_v0, _v1, _v2) {
		return $elm$core$Task$succeed(_Utils_Tuple0);
	});
var $elm$core$Task$cmdMap = F2(
	function (tagger, _v0) {
		var task = _v0.a;
		return $elm$core$Task$Perform(
			A2($elm$core$Task$map, tagger, task));
	});
_Platform_effectManagers['Task'] = _Platform_createManager($elm$core$Task$init, $elm$core$Task$onEffects, $elm$core$Task$onSelfMsg, $elm$core$Task$cmdMap);
var $elm$core$Task$command = _Platform_leaf('Task');
var $elm$core$Task$perform = F2(
	function (toMessage, task) {
		return $elm$core$Task$command(
			$elm$core$Task$Perform(
				A2($elm$core$Task$map, toMessage, task)));
	});
var $elm$browser$Browser$element = _Browser_element;
var $elm$core$Basics$min = F2(
	function (x, y) {
		return (_Utils_cmp(x, y) < 0) ? x : y;
	});
var $author$project$Canvas$computeScaleFactor = function (converter) {
	var valueBound = converter.valueBounding;
	var valueRangeX = valueBound.maxX - valueBound.minX;
	var valueRangeY = valueBound.maxY - valueBound.minY;
	var canvasBound = converter.canvasBounding;
	var canvasHeight = canvasBound.maxY - canvasBound.minY;
	var canvasWidth = canvasBound.maxX - canvasBound.minX;
	var scaleFactor = ((0.0 < valueRangeX) && (0.0 < valueRangeY)) ? A2($elm$core$Basics$min, canvasWidth / valueRangeX, canvasHeight / valueRangeY) : ((0.0 < valueRangeX) ? (canvasWidth / valueRangeX) : ((0.0 < valueRangeY) ? (canvasHeight / valueRangeY) : 1.0));
	return scaleFactor;
};
var $author$project$Canvas$coordinateConversion = function (converter) {
	return function (_v0) {
		var x = _v0.a;
		var y = _v0.b;
		var valueBound = converter.valueBounding;
		var scaleFactor = $author$project$Canvas$computeScaleFactor(converter);
		var canvasBound = converter.canvasBounding;
		var translateX = canvasBound.minX + (scaleFactor * (x - valueBound.minX));
		var translateY = canvasBound.minY + (scaleFactor * (valueBound.maxY - y));
		return _Utils_Tuple3(translateX, translateY, scaleFactor);
	};
};
var $author$project$Canvas$coordinateConvertCircle = F2(
	function (converter, circle) {
		var _v0 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(circle.cx, circle.cy));
		var newX = _v0.a;
		var newY = _v0.b;
		var scaleFactor = _v0.c;
		return _Utils_update(
			circle,
			{cx: newX, cy: newY, radius: scaleFactor * circle.radius});
	});
var $author$project$Canvas$coordinateConvertContourLine = F2(
	function (converter, cline) {
		var line = cline.line;
		var _v0 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(line.x2, line.y2));
		var newX2 = _v0.a;
		var newY2 = _v0.b;
		var _v1 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(line.x1, line.y1));
		var newX1 = _v1.a;
		var newY1 = _v1.b;
		var newLine = _Utils_update(
			line,
			{x1: newX1, x2: newX2, y1: newY1, y2: newY2});
		return _Utils_update(
			cline,
			{line: newLine});
	});
var $author$project$Canvas$coordinateConvertContourPolygon = F2(
	function (converter, cpolygon) {
		var polygon = cpolygon.polygon;
		var newPoints = A2(
			$elm$core$List$map,
			function (p) {
				var _v0 = A2(
					$author$project$Canvas$coordinateConversion,
					converter,
					_Utils_Tuple2(p.x, p.y));
				var x = _v0.a;
				var y = _v0.b;
				return _Utils_update(
					p,
					{x: x, y: y});
			},
			polygon.points);
		var newPolygon = _Utils_update(
			polygon,
			{points: newPoints});
		return _Utils_update(
			cpolygon,
			{polygon: newPolygon});
	});
var $author$project$Canvas$coordinateConvertLine = F2(
	function (converter, line) {
		var _v0 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(line.x2, line.y2));
		var newX2 = _v0.a;
		var newY2 = _v0.b;
		var _v1 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(line.x1, line.y1));
		var newX1 = _v1.a;
		var newY1 = _v1.b;
		return _Utils_update(
			line,
			{x1: newX1, x2: newX2, y1: newY1, y2: newY2});
	});
var $author$project$Canvas$coordinateConvertLineText = F2(
	function (converter, lineText) {
		var _v0 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(lineText.x2, lineText.y2));
		var newX2 = _v0.a;
		var newY2 = _v0.b;
		var _v1 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(lineText.x1, lineText.y1));
		var newX1 = _v1.a;
		var newY1 = _v1.b;
		return _Utils_update(
			lineText,
			{x1: newX1, x2: newX2, y1: newY1, y2: newY2});
	});
var $author$project$Canvas$coordinateConvertMomentLine = F2(
	function (converter, mline) {
		var newLine = A2($author$project$Canvas$coordinateConvertLine, converter, mline.line);
		return _Utils_update(
			mline,
			{line: newLine});
	});
var $author$project$Canvas$coordinateConvertPolygon = F2(
	function (converter, polygon) {
		var newPoints = A2(
			$elm$core$List$map,
			function (p) {
				var _v0 = A2(
					$author$project$Canvas$coordinateConversion,
					converter,
					_Utils_Tuple2(p.x, p.y));
				var x = _v0.a;
				var y = _v0.b;
				return _Utils_update(
					p,
					{x: x, y: y});
			},
			polygon.points);
		return _Utils_update(
			polygon,
			{points: newPoints});
	});
var $author$project$Canvas$coordinateConvertRectangle = F2(
	function (converter, rect) {
		var _v0 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(rect.x, rect.y));
		var newX = _v0.a;
		var newY = _v0.b;
		var scaleFactor = _v0.c;
		return _Utils_update(
			rect,
			{height: rect.height * scaleFactor, width: rect.width * scaleFactor, x: newX, y: newY});
	});
var $author$project$Canvas$coordinateConvertScalableCircle = F2(
	function (converter, scircle) {
		var circle = scircle.circle;
		var _v0 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(circle.cx, circle.cy));
		var newX = _v0.a;
		var newY = _v0.b;
		var newCircle = _Utils_update(
			circle,
			{cx: newX, cy: newY, radius: scircle.circle.radius, style: scircle.circle.style});
		return _Utils_update(
			scircle,
			{circle: newCircle});
	});
var $author$project$Canvas$coordinateConvertScalableLine = F2(
	function (converter, sline) {
		var line = sline.line;
		var _v0 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(line.x2, line.y2));
		var newX2 = _v0.a;
		var newY2 = _v0.b;
		var _v1 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(line.x1, line.y1));
		var newX1 = _v1.a;
		var newY1 = _v1.b;
		var newLine = _Utils_update(
			line,
			{x1: newX1, x2: newX2, y1: newY1, y2: newY2});
		return _Utils_update(
			sline,
			{line: newLine});
	});
var $author$project$Canvas$coordinateConvertText = F2(
	function (converter, text) {
		var _v0 = A2(
			$author$project$Canvas$coordinateConversion,
			converter,
			_Utils_Tuple2(text.x, text.y));
		var newX = _v0.a;
		var newY = _v0.b;
		return _Utils_update(
			text,
			{x: newX, y: newY});
	});
var $author$project$Canvas$coordinateConvertLayer = F2(
	function (converter, layer) {
		return _Utils_update(
			layer,
			{
				circles: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertCircle(converter),
					layer.circles),
				contourLines: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertContourLine(converter),
					layer.contourLines),
				contourPolygons: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertContourPolygon(converter),
					layer.contourPolygons),
				lineTexts: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertLineText(converter),
					layer.lineTexts),
				lines: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertLine(converter),
					layer.lines),
				momentLines: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertMomentLine(converter),
					layer.momentLines),
				polygons: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertPolygon(converter),
					layer.polygons),
				rectangles: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertRectangle(converter),
					layer.rectangles),
				scalableCircles: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertScalableCircle(converter),
					layer.scalableCircles),
				scalableLines: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertScalableLine(converter),
					layer.scalableLines),
				texts: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertText(converter),
					layer.texts)
			});
	});
var $author$project$Canvas$coordinateConvertEntities = F2(
	function (converter, entities) {
		return _Utils_update(
			entities,
			{
				layers: A2(
					$elm$core$List$map,
					$author$project$Canvas$coordinateConvertLayer(converter),
					entities.layers),
				xaxes: A2(
					$elm$core$List$map,
					function (axis) {
						var _v0 = A2(
							$author$project$Canvas$coordinateConversion,
							converter,
							_Utils_Tuple2(axis.position, 0.0));
						var x = _v0.a;
						return _Utils_update(
							axis,
							{position: x});
					},
					entities.xaxes),
				yaxes: A2(
					$elm$core$List$map,
					function (axis) {
						var _v1 = A2(
							$author$project$Canvas$coordinateConversion,
							converter,
							_Utils_Tuple2(0.0, axis.position));
						var y = _v1.b;
						return _Utils_update(
							axis,
							{position: y});
					},
					entities.yaxes)
			});
	});
var $author$project$Canvas$boundingCircle = function (circle) {
	return {maxX: circle.cx + circle.radius, maxY: circle.cy + circle.radius, minX: circle.cx - circle.radius, minY: circle.cy - circle.radius};
};
var $author$project$Canvas$boundingLine = function (line) {
	return {
		maxX: A2($elm$core$Basics$max, line.x1, line.x2),
		maxY: A2($elm$core$Basics$max, line.y1, line.y2),
		minX: A2($elm$core$Basics$min, line.x1, line.x2),
		minY: A2($elm$core$Basics$min, line.y1, line.y2)
	};
};
var $elm$core$List$maximum = function (list) {
	if (list.b) {
		var x = list.a;
		var xs = list.b;
		return $elm$core$Maybe$Just(
			A3($elm$core$List$foldl, $elm$core$Basics$max, x, xs));
	} else {
		return $elm$core$Maybe$Nothing;
	}
};
var $elm$core$List$minimum = function (list) {
	if (list.b) {
		var x = list.a;
		var xs = list.b;
		return $elm$core$Maybe$Just(
			A3($elm$core$List$foldl, $elm$core$Basics$min, x, xs));
	} else {
		return $elm$core$Maybe$Nothing;
	}
};
var $author$project$Canvas$boundingPolygon = function (polygon) {
	var ys = A2(
		$elm$core$List$map,
		function (p) {
			return p.y;
		},
		polygon.points);
	var xs = A2(
		$elm$core$List$map,
		function (p) {
			return p.x;
		},
		polygon.points);
	var getValue = function (value) {
		if (value.$ === 'Just') {
			var v = value.a;
			return v;
		} else {
			return 0.0;
		}
	};
	return {
		maxX: getValue(
			$elm$core$List$maximum(xs)),
		maxY: getValue(
			$elm$core$List$maximum(ys)),
		minX: getValue(
			$elm$core$List$minimum(xs)),
		minY: getValue(
			$elm$core$List$minimum(ys))
	};
};
var $author$project$Canvas$boundingRectangle = function (rect) {
	return {maxX: rect.x + (0.5 * rect.width), maxY: rect.y + (0.5 * rect.height), minX: rect.x - (0.5 * rect.width), minY: rect.y - (0.5 * rect.height)};
};
var $author$project$Canvas$boundingText = function (text) {
	return {maxX: text.x, maxY: text.y, minX: text.x, minY: text.y};
};
var $elm$core$List$append = F2(
	function (xs, ys) {
		if (!ys.b) {
			return xs;
		} else {
			return A3($elm$core$List$foldr, $elm$core$List$cons, ys, xs);
		}
	});
var $elm$core$List$concat = function (lists) {
	return A3($elm$core$List$foldr, $elm$core$List$append, _List_Nil, lists);
};
var $elm$core$List$concatMap = F2(
	function (f, list) {
		return $elm$core$List$concat(
			A2($elm$core$List$map, f, list));
	});
var $elm$core$Maybe$withDefault = F2(
	function (_default, maybe) {
		if (maybe.$ === 'Just') {
			var value = maybe.a;
			return value;
		} else {
			return _default;
		}
	});
var $author$project$Canvas$mergeBounding = function (boundingRects) {
	var ys = A2(
		$elm$core$List$concatMap,
		function (rect) {
			return _List_fromArray(
				[rect.minY, rect.maxY]);
		},
		boundingRects);
	var xs = A2(
		$elm$core$List$concatMap,
		function (rect) {
			return _List_fromArray(
				[rect.minX, rect.maxX]);
		},
		boundingRects);
	return {
		maxX: A2(
			$elm$core$Maybe$withDefault,
			0.0,
			$elm$core$List$maximum(xs)),
		maxY: A2(
			$elm$core$Maybe$withDefault,
			0.0,
			$elm$core$List$maximum(ys)),
		minX: A2(
			$elm$core$Maybe$withDefault,
			0.0,
			$elm$core$List$minimum(xs)),
		minY: A2(
			$elm$core$Maybe$withDefault,
			0.0,
			$elm$core$List$minimum(ys))
	};
};
var $author$project$Canvas$boundingLayer = function (layer) {
	return $author$project$Canvas$mergeBounding(
		$elm$core$List$concat(
			_List_fromArray(
				[
					A2($elm$core$List$map, $author$project$Canvas$boundingLine, layer.lines),
					A2($elm$core$List$map, $author$project$Canvas$boundingCircle, layer.circles),
					A2($elm$core$List$map, $author$project$Canvas$boundingRectangle, layer.rectangles),
					A2($elm$core$List$map, $author$project$Canvas$boundingPolygon, layer.polygons),
					A2(
					$elm$core$List$map,
					function (sline) {
						return $author$project$Canvas$boundingLine(sline.line);
					},
					layer.scalableLines),
					A2(
					$elm$core$List$map,
					function (scircle) {
						return $author$project$Canvas$boundingCircle(scircle.circle);
					},
					layer.scalableCircles),
					A2($elm$core$List$map, $author$project$Canvas$boundingText, layer.texts)
				])));
};
var $author$project$Canvas$getCoordinateConverter = function (model) {
	var entities = model.entities;
	var valueBound = $author$project$Canvas$mergeBounding(
		A2($elm$core$List$map, $author$project$Canvas$boundingLayer, entities.layers));
	var config = model.config;
	return {
		canvasBounding: {maxX: config.width - config.margin, maxY: config.height - config.margin, minX: config.margin, minY: config.margin},
		valueBounding: valueBound
	};
};
var $author$project$Canvas$coordinateConvertModel = function (model) {
	var converter = $author$project$Canvas$getCoordinateConverter(model);
	return _Utils_update(
		model,
		{
			entities: A2($author$project$Canvas$coordinateConvertEntities, converter, model.entities)
		});
};
var $author$project$Canvas$Flags = F5(
	function (config, entities, tree, labels, tags) {
		return {config: config, entities: entities, labels: labels, tags: tags, tree: tree};
	});
var $author$project$Canvas$Config = function (zoom) {
	return function (centerX) {
		return function (centerY) {
			return function (width) {
				return function (height) {
					return function (margin) {
						return function (fontSize) {
							return function (scalableFactors) {
								return function (contourMin) {
									return function (contourMax) {
										return function (visibleColorBar) {
											return function (colorBarX) {
												return function (colorBarY) {
													return function (enabledCoordinateConversion) {
														return function (descriptions) {
															return {centerX: centerX, centerY: centerY, colorBarX: colorBarX, colorBarY: colorBarY, contourMax: contourMax, contourMin: contourMin, descriptions: descriptions, enabledCoordinateConversion: enabledCoordinateConversion, fontSize: fontSize, height: height, margin: margin, scalableFactors: scalableFactors, visibleColorBar: visibleColorBar, width: width, zoom: zoom};
														};
													};
												};
											};
										};
									};
								};
							};
						};
					};
				};
			};
		};
	};
};
var $elm$json$Json$Decode$bool = _Json_decodeBool;
var $author$project$Canvas$ScalableFactors = F3(
	function (momentLine, scalableLine, scalableCircle) {
		return {momentLine: momentLine, scalableCircle: scalableCircle, scalableLine: scalableLine};
	});
var $elm$json$Json$Decode$float = _Json_decodeFloat;
var $NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$custom = $elm$json$Json$Decode$map2($elm$core$Basics$apR);
var $elm$json$Json$Decode$andThen = _Json_andThen;
var $elm$json$Json$Decode$field = _Json_decodeField;
var $elm$json$Json$Decode$at = F2(
	function (fields, decoder) {
		return A3($elm$core$List$foldr, $elm$json$Json$Decode$field, decoder, fields);
	});
var $elm$json$Json$Decode$decodeValue = _Json_run;
var $elm$json$Json$Decode$null = _Json_decodeNull;
var $elm$json$Json$Decode$oneOf = _Json_oneOf;
var $elm$json$Json$Decode$value = _Json_decodeValue;
var $NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optionalDecoder = F3(
	function (path, valDecoder, fallback) {
		var nullOr = function (decoder) {
			return $elm$json$Json$Decode$oneOf(
				_List_fromArray(
					[
						decoder,
						$elm$json$Json$Decode$null(fallback)
					]));
		};
		var handleResult = function (input) {
			var _v0 = A2(
				$elm$json$Json$Decode$decodeValue,
				A2($elm$json$Json$Decode$at, path, $elm$json$Json$Decode$value),
				input);
			if (_v0.$ === 'Ok') {
				var rawValue = _v0.a;
				var _v1 = A2(
					$elm$json$Json$Decode$decodeValue,
					nullOr(valDecoder),
					rawValue);
				if (_v1.$ === 'Ok') {
					var finalResult = _v1.a;
					return $elm$json$Json$Decode$succeed(finalResult);
				} else {
					return A2(
						$elm$json$Json$Decode$at,
						path,
						nullOr(valDecoder));
				}
			} else {
				return $elm$json$Json$Decode$succeed(fallback);
			}
		};
		return A2($elm$json$Json$Decode$andThen, handleResult, $elm$json$Json$Decode$value);
	});
var $NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional = F4(
	function (key, valDecoder, fallback, decoder) {
		return A2(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$custom,
			A3(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optionalDecoder,
				_List_fromArray(
					[key]),
				valDecoder,
				fallback),
			decoder);
	});
var $author$project$Canvas$decodeScalableFactors = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'scalableCircle',
	$elm$json$Json$Decode$float,
	1.0,
	A4(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
		'scalableLine',
		$elm$json$Json$Decode$float,
		1.0,
		A4(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
			'momentLine',
			$elm$json$Json$Decode$float,
			1.0,
			$elm$json$Json$Decode$succeed($author$project$Canvas$ScalableFactors))));
var $author$project$Canvas$defaultScalableFactors = {momentLine: 1.0, scalableCircle: 1.0, scalableLine: 1.0};
var $elm$json$Json$Decode$list = _Json_decodeList;
var $NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required = F3(
	function (key, valDecoder, decoder) {
		return A2(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$custom,
			A2($elm$json$Json$Decode$field, key, valDecoder),
			decoder);
	});
var $elm$json$Json$Decode$string = _Json_decodeString;
var $author$project$Canvas$decodeConfig = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'descriptions',
	$elm$json$Json$Decode$list($elm$json$Json$Decode$string),
	_List_Nil,
	A4(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
		'enabledCoordinateConversion',
		$elm$json$Json$Decode$bool,
		true,
		A4(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
			'colorBarY',
			$elm$json$Json$Decode$float,
			0.0,
			A4(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
				'colorBarX',
				$elm$json$Json$Decode$float,
				0.0,
				A4(
					$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
					'visibleColorBar',
					$elm$json$Json$Decode$bool,
					false,
					A4(
						$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
						'contourMax',
						$elm$json$Json$Decode$float,
						1.0,
						A4(
							$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
							'contourMin',
							$elm$json$Json$Decode$float,
							0.0,
							A4(
								$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
								'scalableFactors',
								$author$project$Canvas$decodeScalableFactors,
								$author$project$Canvas$defaultScalableFactors,
								A4(
									$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
									'fontSize',
									$elm$json$Json$Decode$float,
									10.0,
									A4(
										$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
										'margin',
										$elm$json$Json$Decode$float,
										20.0,
										A3(
											$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
											'height',
											$elm$json$Json$Decode$float,
											A3(
												$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
												'width',
												$elm$json$Json$Decode$float,
												A3(
													$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
													'centerY',
													$elm$json$Json$Decode$float,
													A3(
														$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
														'centerX',
														$elm$json$Json$Decode$float,
														A4(
															$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
															'zoom',
															$elm$json$Json$Decode$float,
															1.0,
															$elm$json$Json$Decode$succeed($author$project$Canvas$Config))))))))))))))));
var $author$project$Canvas$Entities = F3(
	function (layers, xaxes, yaxes) {
		return {layers: layers, xaxes: xaxes, yaxes: yaxes};
	});
var $author$project$Canvas$Axis = F2(
	function (name, position) {
		return {name: name, position: position};
	});
var $author$project$Canvas$decodeAxis = A3(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
	'position',
	$elm$json$Json$Decode$float,
	A3(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
		'name',
		$elm$json$Json$Decode$string,
		$elm$json$Json$Decode$succeed($author$project$Canvas$Axis)));
var $author$project$Canvas$Layer = function (texts) {
	return function (lines) {
		return function (circles) {
			return function (rectangles) {
				return function (polygons) {
					return function (scalableLines) {
						return function (scalableCircles) {
							return function (contourLines) {
								return function (contourPolygons) {
									return function (momentLines) {
										return function (lineTexts) {
											return {circles: circles, contourLines: contourLines, contourPolygons: contourPolygons, lineTexts: lineTexts, lines: lines, momentLines: momentLines, polygons: polygons, rectangles: rectangles, scalableCircles: scalableCircles, scalableLines: scalableLines, texts: texts};
										};
									};
								};
							};
						};
					};
				};
			};
		};
	};
};
var $author$project$Canvas$Circle = F5(
	function (cx, cy, radius, style, tags) {
		return {cx: cx, cy: cy, radius: radius, style: style, tags: tags};
	});
var $author$project$Canvas$EntityStyle = F4(
	function (stroke, strokeWidth, fill, opacity) {
		return {fill: fill, opacity: opacity, stroke: stroke, strokeWidth: strokeWidth};
	});
var $author$project$Canvas$decodeEntityStyle = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'opacity',
	$elm$json$Json$Decode$float,
	1.0,
	A3(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
		'fill',
		$elm$json$Json$Decode$string,
		A4(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
			'strokeWidth',
			$elm$json$Json$Decode$float,
			1.0,
			A3(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
				'stroke',
				$elm$json$Json$Decode$string,
				$elm$json$Json$Decode$succeed($author$project$Canvas$EntityStyle)))));
var $author$project$Canvas$defaultEntityStyle = {fill: 'transparent', opacity: 1.0, stroke: 'black', strokeWidth: 1.0};
var $author$project$Canvas$decodeCircle = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'tags',
	$elm$json$Json$Decode$list($elm$json$Json$Decode$string),
	_List_Nil,
	A4(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
		'style',
		$author$project$Canvas$decodeEntityStyle,
		$author$project$Canvas$defaultEntityStyle,
		A3(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
			'radius',
			$elm$json$Json$Decode$float,
			A3(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
				'cy',
				$elm$json$Json$Decode$float,
				A3(
					$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
					'cx',
					$elm$json$Json$Decode$float,
					$elm$json$Json$Decode$succeed($author$project$Canvas$Circle))))));
var $author$project$Canvas$ContourLine = F2(
	function (line, value) {
		return {line: line, value: value};
	});
var $author$project$Canvas$Line = F7(
	function (x1, y1, x2, y2, stroke, strokeWidth, tags) {
		return {stroke: stroke, strokeWidth: strokeWidth, tags: tags, x1: x1, x2: x2, y1: y1, y2: y2};
	});
var $author$project$Canvas$decodeLine = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'tags',
	$elm$json$Json$Decode$list($elm$json$Json$Decode$string),
	_List_Nil,
	A4(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
		'strokeWidth',
		$elm$json$Json$Decode$float,
		1.0,
		A4(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
			'stroke',
			$elm$json$Json$Decode$string,
			'black',
			A3(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
				'y2',
				$elm$json$Json$Decode$float,
				A3(
					$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
					'x2',
					$elm$json$Json$Decode$float,
					A3(
						$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
						'y1',
						$elm$json$Json$Decode$float,
						A3(
							$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
							'x1',
							$elm$json$Json$Decode$float,
							$elm$json$Json$Decode$succeed($author$project$Canvas$Line))))))));
var $author$project$Canvas$decodeContourLine = A3(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
	'value',
	$elm$json$Json$Decode$float,
	A3(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
		'line',
		$author$project$Canvas$decodeLine,
		$elm$json$Json$Decode$succeed($author$project$Canvas$ContourLine)));
var $author$project$Canvas$ContourPolygon = F2(
	function (polygon, value) {
		return {polygon: polygon, value: value};
	});
var $author$project$Canvas$Polygon = F3(
	function (points, style, tags) {
		return {points: points, style: style, tags: tags};
	});
var $author$project$Canvas$Point = F3(
	function (x, y, tags) {
		return {tags: tags, x: x, y: y};
	});
var $author$project$Canvas$decodePoint = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'tags',
	$elm$json$Json$Decode$list($elm$json$Json$Decode$string),
	_List_Nil,
	A3(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
		'y',
		$elm$json$Json$Decode$float,
		A3(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
			'x',
			$elm$json$Json$Decode$float,
			$elm$json$Json$Decode$succeed($author$project$Canvas$Point))));
var $author$project$Canvas$decodePolygon = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'tags',
	$elm$json$Json$Decode$list($elm$json$Json$Decode$string),
	_List_Nil,
	A3(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
		'style',
		$author$project$Canvas$decodeEntityStyle,
		A3(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
			'points',
			$elm$json$Json$Decode$list($author$project$Canvas$decodePoint),
			$elm$json$Json$Decode$succeed($author$project$Canvas$Polygon))));
var $author$project$Canvas$decodeContourPolygon = A3(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
	'value',
	$elm$json$Json$Decode$float,
	A3(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
		'polygon',
		$author$project$Canvas$decodePolygon,
		$elm$json$Json$Decode$succeed($author$project$Canvas$ContourPolygon)));
var $author$project$Canvas$LineText = function (text) {
	return function (x1) {
		return function (y1) {
			return function (x2) {
				return function (y2) {
					return function (ratio) {
						return function (stroke) {
							return function (fill) {
								return function (rotate) {
									return function (textAnchor) {
										return function (dominantBaseLine) {
											return function (offsetFontHeight) {
												return function (tags) {
													return {dominantBaseLine: dominantBaseLine, fill: fill, offsetFontHeight: offsetFontHeight, ratio: ratio, rotate: rotate, stroke: stroke, tags: tags, text: text, textAnchor: textAnchor, x1: x1, x2: x2, y1: y1, y2: y2};
												};
											};
										};
									};
								};
							};
						};
					};
				};
			};
		};
	};
};
var $author$project$Canvas$decodeLineText = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'tags',
	$elm$json$Json$Decode$list($elm$json$Json$Decode$string),
	_List_Nil,
	A4(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
		'offsetFontHeight',
		$elm$json$Json$Decode$float,
		0.0,
		A4(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
			'dominantBaseLine',
			$elm$json$Json$Decode$string,
			'auto',
			A4(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
				'textAnchor',
				$elm$json$Json$Decode$string,
				'start',
				A4(
					$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
					'rotate',
					$elm$json$Json$Decode$float,
					0.0,
					A4(
						$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
						'fill',
						$elm$json$Json$Decode$string,
						'black',
						A4(
							$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
							'stroke',
							$elm$json$Json$Decode$string,
							'black',
							A3(
								$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
								'ratio',
								$elm$json$Json$Decode$float,
								A3(
									$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
									'y2',
									$elm$json$Json$Decode$float,
									A3(
										$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
										'x2',
										$elm$json$Json$Decode$float,
										A3(
											$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
											'y1',
											$elm$json$Json$Decode$float,
											A3(
												$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
												'x1',
												$elm$json$Json$Decode$float,
												A3(
													$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
													'text',
													$elm$json$Json$Decode$string,
													$elm$json$Json$Decode$succeed($author$project$Canvas$LineText))))))))))))));
var $author$project$Canvas$MomentLine = F4(
	function (m1, m2, m0, line) {
		return {line: line, m0: m0, m1: m1, m2: m2};
	});
var $author$project$Canvas$decodeMomentLine = A3(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
	'line',
	$author$project$Canvas$decodeLine,
	A4(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
		'm0',
		$elm$json$Json$Decode$float,
		0.0,
		A3(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
			'm2',
			$elm$json$Json$Decode$float,
			A3(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
				'm1',
				$elm$json$Json$Decode$float,
				$elm$json$Json$Decode$succeed($author$project$Canvas$MomentLine)))));
var $author$project$Canvas$Rectangle = F6(
	function (x, y, width, height, style, tags) {
		return {height: height, style: style, tags: tags, width: width, x: x, y: y};
	});
var $author$project$Canvas$decodeRectangle = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'tags',
	$elm$json$Json$Decode$list($elm$json$Json$Decode$string),
	_List_Nil,
	A4(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
		'style',
		$author$project$Canvas$decodeEntityStyle,
		$author$project$Canvas$defaultEntityStyle,
		A3(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
			'height',
			$elm$json$Json$Decode$float,
			A3(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
				'width',
				$elm$json$Json$Decode$float,
				A3(
					$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
					'y',
					$elm$json$Json$Decode$float,
					A3(
						$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
						'x',
						$elm$json$Json$Decode$float,
						$elm$json$Json$Decode$succeed($author$project$Canvas$Rectangle)))))));
var $author$project$Canvas$ScalableCircle = F2(
	function (circle, value) {
		return {circle: circle, value: value};
	});
var $author$project$Canvas$decodeScalableCircle = A3(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
	'value',
	$elm$json$Json$Decode$float,
	A3(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
		'circle',
		$author$project$Canvas$decodeCircle,
		$elm$json$Json$Decode$succeed($author$project$Canvas$ScalableCircle)));
var $author$project$Canvas$ScalableLine = F5(
	function (line, dx1, dy1, dx2, dy2) {
		return {dx1: dx1, dx2: dx2, dy1: dy1, dy2: dy2, line: line};
	});
var $author$project$Canvas$decodeScalableLine = A3(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
	'dy2',
	$elm$json$Json$Decode$float,
	A3(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
		'dx2',
		$elm$json$Json$Decode$float,
		A3(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
			'dy1',
			$elm$json$Json$Decode$float,
			A3(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
				'dx1',
				$elm$json$Json$Decode$float,
				A3(
					$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
					'line',
					$author$project$Canvas$decodeLine,
					$elm$json$Json$Decode$succeed($author$project$Canvas$ScalableLine))))));
var $author$project$Canvas$Text = function (text) {
	return function (x) {
		return function (y) {
			return function (stroke) {
				return function (fill) {
					return function (rotate) {
						return function (textAnchor) {
							return function (dominantBaseLine) {
								return function (offsetFontHeight) {
									return function (tags) {
										return {dominantBaseLine: dominantBaseLine, fill: fill, offsetFontHeight: offsetFontHeight, rotate: rotate, stroke: stroke, tags: tags, text: text, textAnchor: textAnchor, x: x, y: y};
									};
								};
							};
						};
					};
				};
			};
		};
	};
};
var $author$project$Canvas$decodeText = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'tags',
	$elm$json$Json$Decode$list($elm$json$Json$Decode$string),
	_List_Nil,
	A4(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
		'offsetFontHeight',
		$elm$json$Json$Decode$float,
		0.0,
		A4(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
			'dominantBaseLine',
			$elm$json$Json$Decode$string,
			'auto',
			A4(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
				'textAnchor',
				$elm$json$Json$Decode$string,
				'start',
				A4(
					$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
					'rotate',
					$elm$json$Json$Decode$float,
					0.0,
					A4(
						$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
						'fill',
						$elm$json$Json$Decode$string,
						'black',
						A4(
							$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
							'stroke',
							$elm$json$Json$Decode$string,
							'black',
							A3(
								$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
								'y',
								$elm$json$Json$Decode$float,
								A3(
									$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
									'x',
									$elm$json$Json$Decode$float,
									A3(
										$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
										'text',
										$elm$json$Json$Decode$string,
										$elm$json$Json$Decode$succeed($author$project$Canvas$Text)))))))))));
var $author$project$Canvas$decodeLayer = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'lineTexts',
	$elm$json$Json$Decode$list($author$project$Canvas$decodeLineText),
	_List_Nil,
	A4(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
		'momentLines',
		$elm$json$Json$Decode$list($author$project$Canvas$decodeMomentLine),
		_List_Nil,
		A4(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
			'contourPolygons',
			$elm$json$Json$Decode$list($author$project$Canvas$decodeContourPolygon),
			_List_Nil,
			A4(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
				'contourLines',
				$elm$json$Json$Decode$list($author$project$Canvas$decodeContourLine),
				_List_Nil,
				A4(
					$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
					'scalableCircles',
					$elm$json$Json$Decode$list($author$project$Canvas$decodeScalableCircle),
					_List_Nil,
					A4(
						$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
						'scalableLines',
						$elm$json$Json$Decode$list($author$project$Canvas$decodeScalableLine),
						_List_Nil,
						A4(
							$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
							'polygons',
							$elm$json$Json$Decode$list($author$project$Canvas$decodePolygon),
							_List_Nil,
							A4(
								$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
								'rectangles',
								$elm$json$Json$Decode$list($author$project$Canvas$decodeRectangle),
								_List_Nil,
								A4(
									$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
									'circles',
									$elm$json$Json$Decode$list($author$project$Canvas$decodeCircle),
									_List_Nil,
									A4(
										$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
										'lines',
										$elm$json$Json$Decode$list($author$project$Canvas$decodeLine),
										_List_Nil,
										A4(
											$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
											'texts',
											$elm$json$Json$Decode$list($author$project$Canvas$decodeText),
											_List_Nil,
											$elm$json$Json$Decode$succeed($author$project$Canvas$Layer))))))))))));
var $author$project$Canvas$decodeEntities = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'yaxes',
	$elm$json$Json$Decode$list($author$project$Canvas$decodeAxis),
	_List_Nil,
	A4(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
		'xaxes',
		$elm$json$Json$Decode$list($author$project$Canvas$decodeAxis),
		_List_Nil,
		A4(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
			'layers',
			$elm$json$Json$Decode$list($author$project$Canvas$decodeLayer),
			_List_Nil,
			$elm$json$Json$Decode$succeed($author$project$Canvas$Entities))));
var $author$project$Canvas$Label = F2(
	function (no, name) {
		return {name: name, no: no};
	});
var $elm$json$Json$Decode$int = _Json_decodeInt;
var $author$project$Canvas$decodeLabel = A3(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
	'name',
	$elm$json$Json$Decode$string,
	A3(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
		'no',
		$elm$json$Json$Decode$int,
		$elm$json$Json$Decode$succeed($author$project$Canvas$Label)));
var $author$project$Canvas$Tag = F3(
	function (key, displayName, activated) {
		return {activated: activated, displayName: displayName, key: key};
	});
var $author$project$Canvas$decodeTag = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'activated',
	$elm$json$Json$Decode$bool,
	false,
	A3(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
		'displayName',
		$elm$json$Json$Decode$string,
		A3(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
			'key',
			$elm$json$Json$Decode$string,
			$elm$json$Json$Decode$succeed($author$project$Canvas$Tag))));
var $author$project$Canvas$TreeItem = F3(
	function (path, displayName, labelNames) {
		return {displayName: displayName, labelNames: labelNames, path: path};
	});
var $author$project$Canvas$decodeTreeItem = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'labelNames',
	$elm$json$Json$Decode$list($elm$json$Json$Decode$string),
	_List_Nil,
	A3(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
		'displayName',
		$elm$json$Json$Decode$string,
		A3(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
			'path',
			$elm$json$Json$Decode$string,
			$elm$json$Json$Decode$succeed($author$project$Canvas$TreeItem))));
var $author$project$Canvas$defaultConfig = {centerX: 1.0, centerY: 1.0, colorBarX: 1.0, colorBarY: 1.0, contourMax: 1.0, contourMin: 1.0, descriptions: _List_Nil, enabledCoordinateConversion: false, fontSize: 1.0, height: 1.0, margin: 1.0, scalableFactors: $author$project$Canvas$defaultScalableFactors, visibleColorBar: false, width: 1.0, zoom: 1.0};
var $author$project$Canvas$decodeFlags = A4(
	$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
	'tags',
	$elm$json$Json$Decode$list($author$project$Canvas$decodeTag),
	_List_Nil,
	A4(
		$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
		'labels',
		$elm$json$Json$Decode$list($author$project$Canvas$decodeLabel),
		_List_Nil,
		A4(
			$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
			'tree',
			$elm$json$Json$Decode$list($author$project$Canvas$decodeTreeItem),
			_List_Nil,
			A3(
				$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$required,
				'entities',
				$author$project$Canvas$decodeEntities,
				A4(
					$NoRedInk$elm_json_decode_pipeline$Json$Decode$Pipeline$optional,
					'config',
					$author$project$Canvas$decodeConfig,
					$author$project$Canvas$defaultConfig,
					$elm$json$Json$Decode$succeed($author$project$Canvas$Flags))))));
var $zaboco$elm_draggable$Internal$NotDragging = {$: 'NotDragging'};
var $zaboco$elm_draggable$Draggable$State = function (a) {
	return {$: 'State', a: a};
};
var $zaboco$elm_draggable$Draggable$init = $zaboco$elm_draggable$Draggable$State($zaboco$elm_draggable$Internal$NotDragging);
var $elm$core$Debug$log = _Debug_log;
var $elm$core$Platform$Cmd$batch = _Platform_batch;
var $elm$core$Platform$Cmd$none = $elm$core$Platform$Cmd$batch(_List_Nil);
var $author$project$Canvas$init = function (encodedFlags) {
	var model = function () {
		var _v0 = A2($elm$json$Json$Decode$decodeValue, $author$project$Canvas$decodeFlags, encodedFlags);
		if (_v0.$ === 'Err') {
			var err = _v0.a;
			var _v1 = A2($elm$core$Debug$log, 'init error:', err);
			return {
				config: $author$project$Canvas$defaultConfig,
				drag: $zaboco$elm_draggable$Draggable$init,
				entities: {layers: _List_Nil, xaxes: _List_Nil, yaxes: _List_Nil},
				initialConfig: $author$project$Canvas$defaultConfig,
				labels: _List_Nil,
				storageRequestKey: '',
				tags: _List_Nil,
				tree: _List_Nil
			};
		} else {
			var flags = _v0.a;
			var _v2 = A2($elm$core$Debug$log, 'init success:', flags);
			return {config: flags.config, drag: $zaboco$elm_draggable$Draggable$init, entities: flags.entities, initialConfig: flags.config, labels: flags.labels, storageRequestKey: '', tags: flags.tags, tree: flags.tree};
		}
	}();
	var entities = model.entities;
	var config = model.config;
	var newModel = config.enabledCoordinateConversion ? $author$project$Canvas$coordinateConvertModel(model) : model;
	return _Utils_Tuple2(newModel, $elm$core$Platform$Cmd$none);
};
var $author$project$Canvas$DragMsg = function (a) {
	return {$: 'DragMsg', a: a};
};
var $elm$core$Platform$Sub$batch = _Platform_batch;
var $zaboco$elm_draggable$Internal$DragAt = function (a) {
	return {$: 'DragAt', a: a};
};
var $zaboco$elm_draggable$Draggable$Msg = function (a) {
	return {$: 'Msg', a: a};
};
var $zaboco$elm_draggable$Internal$StopDragging = {$: 'StopDragging'};
var $elm$core$Basics$composeL = F3(
	function (g, f, x) {
		return g(
			f(x));
	});
var $elm$core$Platform$Sub$map = _Platform_map;
var $elm$core$Platform$Sub$none = $elm$core$Platform$Sub$batch(_List_Nil);
var $elm$browser$Browser$Events$Document = {$: 'Document'};
var $elm$browser$Browser$Events$MySub = F3(
	function (a, b, c) {
		return {$: 'MySub', a: a, b: b, c: c};
	});
var $elm$browser$Browser$Events$State = F2(
	function (subs, pids) {
		return {pids: pids, subs: subs};
	});
var $elm$core$Dict$RBEmpty_elm_builtin = {$: 'RBEmpty_elm_builtin'};
var $elm$core$Dict$empty = $elm$core$Dict$RBEmpty_elm_builtin;
var $elm$browser$Browser$Events$init = $elm$core$Task$succeed(
	A2($elm$browser$Browser$Events$State, _List_Nil, $elm$core$Dict$empty));
var $elm$browser$Browser$Events$nodeToKey = function (node) {
	if (node.$ === 'Document') {
		return 'd_';
	} else {
		return 'w_';
	}
};
var $elm$browser$Browser$Events$addKey = function (sub) {
	var node = sub.a;
	var name = sub.b;
	return _Utils_Tuple2(
		_Utils_ap(
			$elm$browser$Browser$Events$nodeToKey(node),
			name),
		sub);
};
var $elm$core$Dict$Black = {$: 'Black'};
var $elm$core$Dict$RBNode_elm_builtin = F5(
	function (a, b, c, d, e) {
		return {$: 'RBNode_elm_builtin', a: a, b: b, c: c, d: d, e: e};
	});
var $elm$core$Dict$Red = {$: 'Red'};
var $elm$core$Dict$balance = F5(
	function (color, key, value, left, right) {
		if ((right.$ === 'RBNode_elm_builtin') && (right.a.$ === 'Red')) {
			var _v1 = right.a;
			var rK = right.b;
			var rV = right.c;
			var rLeft = right.d;
			var rRight = right.e;
			if ((left.$ === 'RBNode_elm_builtin') && (left.a.$ === 'Red')) {
				var _v3 = left.a;
				var lK = left.b;
				var lV = left.c;
				var lLeft = left.d;
				var lRight = left.e;
				return A5(
					$elm$core$Dict$RBNode_elm_builtin,
					$elm$core$Dict$Red,
					key,
					value,
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Black, lK, lV, lLeft, lRight),
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Black, rK, rV, rLeft, rRight));
			} else {
				return A5(
					$elm$core$Dict$RBNode_elm_builtin,
					color,
					rK,
					rV,
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, key, value, left, rLeft),
					rRight);
			}
		} else {
			if ((((left.$ === 'RBNode_elm_builtin') && (left.a.$ === 'Red')) && (left.d.$ === 'RBNode_elm_builtin')) && (left.d.a.$ === 'Red')) {
				var _v5 = left.a;
				var lK = left.b;
				var lV = left.c;
				var _v6 = left.d;
				var _v7 = _v6.a;
				var llK = _v6.b;
				var llV = _v6.c;
				var llLeft = _v6.d;
				var llRight = _v6.e;
				var lRight = left.e;
				return A5(
					$elm$core$Dict$RBNode_elm_builtin,
					$elm$core$Dict$Red,
					lK,
					lV,
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Black, llK, llV, llLeft, llRight),
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Black, key, value, lRight, right));
			} else {
				return A5($elm$core$Dict$RBNode_elm_builtin, color, key, value, left, right);
			}
		}
	});
var $elm$core$Basics$compare = _Utils_compare;
var $elm$core$Dict$insertHelp = F3(
	function (key, value, dict) {
		if (dict.$ === 'RBEmpty_elm_builtin') {
			return A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, key, value, $elm$core$Dict$RBEmpty_elm_builtin, $elm$core$Dict$RBEmpty_elm_builtin);
		} else {
			var nColor = dict.a;
			var nKey = dict.b;
			var nValue = dict.c;
			var nLeft = dict.d;
			var nRight = dict.e;
			var _v1 = A2($elm$core$Basics$compare, key, nKey);
			switch (_v1.$) {
				case 'LT':
					return A5(
						$elm$core$Dict$balance,
						nColor,
						nKey,
						nValue,
						A3($elm$core$Dict$insertHelp, key, value, nLeft),
						nRight);
				case 'EQ':
					return A5($elm$core$Dict$RBNode_elm_builtin, nColor, nKey, value, nLeft, nRight);
				default:
					return A5(
						$elm$core$Dict$balance,
						nColor,
						nKey,
						nValue,
						nLeft,
						A3($elm$core$Dict$insertHelp, key, value, nRight));
			}
		}
	});
var $elm$core$Dict$insert = F3(
	function (key, value, dict) {
		var _v0 = A3($elm$core$Dict$insertHelp, key, value, dict);
		if ((_v0.$ === 'RBNode_elm_builtin') && (_v0.a.$ === 'Red')) {
			var _v1 = _v0.a;
			var k = _v0.b;
			var v = _v0.c;
			var l = _v0.d;
			var r = _v0.e;
			return A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Black, k, v, l, r);
		} else {
			var x = _v0;
			return x;
		}
	});
var $elm$core$Dict$fromList = function (assocs) {
	return A3(
		$elm$core$List$foldl,
		F2(
			function (_v0, dict) {
				var key = _v0.a;
				var value = _v0.b;
				return A3($elm$core$Dict$insert, key, value, dict);
			}),
		$elm$core$Dict$empty,
		assocs);
};
var $elm$core$Process$kill = _Scheduler_kill;
var $elm$core$Dict$foldl = F3(
	function (func, acc, dict) {
		foldl:
		while (true) {
			if (dict.$ === 'RBEmpty_elm_builtin') {
				return acc;
			} else {
				var key = dict.b;
				var value = dict.c;
				var left = dict.d;
				var right = dict.e;
				var $temp$func = func,
					$temp$acc = A3(
					func,
					key,
					value,
					A3($elm$core$Dict$foldl, func, acc, left)),
					$temp$dict = right;
				func = $temp$func;
				acc = $temp$acc;
				dict = $temp$dict;
				continue foldl;
			}
		}
	});
var $elm$core$Dict$merge = F6(
	function (leftStep, bothStep, rightStep, leftDict, rightDict, initialResult) {
		var stepState = F3(
			function (rKey, rValue, _v0) {
				stepState:
				while (true) {
					var list = _v0.a;
					var result = _v0.b;
					if (!list.b) {
						return _Utils_Tuple2(
							list,
							A3(rightStep, rKey, rValue, result));
					} else {
						var _v2 = list.a;
						var lKey = _v2.a;
						var lValue = _v2.b;
						var rest = list.b;
						if (_Utils_cmp(lKey, rKey) < 0) {
							var $temp$rKey = rKey,
								$temp$rValue = rValue,
								$temp$_v0 = _Utils_Tuple2(
								rest,
								A3(leftStep, lKey, lValue, result));
							rKey = $temp$rKey;
							rValue = $temp$rValue;
							_v0 = $temp$_v0;
							continue stepState;
						} else {
							if (_Utils_cmp(lKey, rKey) > 0) {
								return _Utils_Tuple2(
									list,
									A3(rightStep, rKey, rValue, result));
							} else {
								return _Utils_Tuple2(
									rest,
									A4(bothStep, lKey, lValue, rValue, result));
							}
						}
					}
				}
			});
		var _v3 = A3(
			$elm$core$Dict$foldl,
			stepState,
			_Utils_Tuple2(
				$elm$core$Dict$toList(leftDict),
				initialResult),
			rightDict);
		var leftovers = _v3.a;
		var intermediateResult = _v3.b;
		return A3(
			$elm$core$List$foldl,
			F2(
				function (_v4, result) {
					var k = _v4.a;
					var v = _v4.b;
					return A3(leftStep, k, v, result);
				}),
			intermediateResult,
			leftovers);
	});
var $elm$browser$Browser$Events$Event = F2(
	function (key, event) {
		return {event: event, key: key};
	});
var $elm$core$Platform$sendToSelf = _Platform_sendToSelf;
var $elm$browser$Browser$Events$spawn = F3(
	function (router, key, _v0) {
		var node = _v0.a;
		var name = _v0.b;
		var actualNode = function () {
			if (node.$ === 'Document') {
				return _Browser_doc;
			} else {
				return _Browser_window;
			}
		}();
		return A2(
			$elm$core$Task$map,
			function (value) {
				return _Utils_Tuple2(key, value);
			},
			A3(
				_Browser_on,
				actualNode,
				name,
				function (event) {
					return A2(
						$elm$core$Platform$sendToSelf,
						router,
						A2($elm$browser$Browser$Events$Event, key, event));
				}));
	});
var $elm$core$Dict$union = F2(
	function (t1, t2) {
		return A3($elm$core$Dict$foldl, $elm$core$Dict$insert, t2, t1);
	});
var $elm$browser$Browser$Events$onEffects = F3(
	function (router, subs, state) {
		var stepRight = F3(
			function (key, sub, _v6) {
				var deads = _v6.a;
				var lives = _v6.b;
				var news = _v6.c;
				return _Utils_Tuple3(
					deads,
					lives,
					A2(
						$elm$core$List$cons,
						A3($elm$browser$Browser$Events$spawn, router, key, sub),
						news));
			});
		var stepLeft = F3(
			function (_v4, pid, _v5) {
				var deads = _v5.a;
				var lives = _v5.b;
				var news = _v5.c;
				return _Utils_Tuple3(
					A2($elm$core$List$cons, pid, deads),
					lives,
					news);
			});
		var stepBoth = F4(
			function (key, pid, _v2, _v3) {
				var deads = _v3.a;
				var lives = _v3.b;
				var news = _v3.c;
				return _Utils_Tuple3(
					deads,
					A3($elm$core$Dict$insert, key, pid, lives),
					news);
			});
		var newSubs = A2($elm$core$List$map, $elm$browser$Browser$Events$addKey, subs);
		var _v0 = A6(
			$elm$core$Dict$merge,
			stepLeft,
			stepBoth,
			stepRight,
			state.pids,
			$elm$core$Dict$fromList(newSubs),
			_Utils_Tuple3(_List_Nil, $elm$core$Dict$empty, _List_Nil));
		var deadPids = _v0.a;
		var livePids = _v0.b;
		var makeNewPids = _v0.c;
		return A2(
			$elm$core$Task$andThen,
			function (pids) {
				return $elm$core$Task$succeed(
					A2(
						$elm$browser$Browser$Events$State,
						newSubs,
						A2(
							$elm$core$Dict$union,
							livePids,
							$elm$core$Dict$fromList(pids))));
			},
			A2(
				$elm$core$Task$andThen,
				function (_v1) {
					return $elm$core$Task$sequence(makeNewPids);
				},
				$elm$core$Task$sequence(
					A2($elm$core$List$map, $elm$core$Process$kill, deadPids))));
	});
var $elm$core$List$maybeCons = F3(
	function (f, mx, xs) {
		var _v0 = f(mx);
		if (_v0.$ === 'Just') {
			var x = _v0.a;
			return A2($elm$core$List$cons, x, xs);
		} else {
			return xs;
		}
	});
var $elm$core$List$filterMap = F2(
	function (f, xs) {
		return A3(
			$elm$core$List$foldr,
			$elm$core$List$maybeCons(f),
			_List_Nil,
			xs);
	});
var $elm$browser$Browser$Events$onSelfMsg = F3(
	function (router, _v0, state) {
		var key = _v0.key;
		var event = _v0.event;
		var toMessage = function (_v2) {
			var subKey = _v2.a;
			var _v3 = _v2.b;
			var node = _v3.a;
			var name = _v3.b;
			var decoder = _v3.c;
			return _Utils_eq(subKey, key) ? A2(_Browser_decodeEvent, decoder, event) : $elm$core$Maybe$Nothing;
		};
		var messages = A2($elm$core$List$filterMap, toMessage, state.subs);
		return A2(
			$elm$core$Task$andThen,
			function (_v1) {
				return $elm$core$Task$succeed(state);
			},
			$elm$core$Task$sequence(
				A2(
					$elm$core$List$map,
					$elm$core$Platform$sendToApp(router),
					messages)));
	});
var $elm$browser$Browser$Events$subMap = F2(
	function (func, _v0) {
		var node = _v0.a;
		var name = _v0.b;
		var decoder = _v0.c;
		return A3(
			$elm$browser$Browser$Events$MySub,
			node,
			name,
			A2($elm$json$Json$Decode$map, func, decoder));
	});
_Platform_effectManagers['Browser.Events'] = _Platform_createManager($elm$browser$Browser$Events$init, $elm$browser$Browser$Events$onEffects, $elm$browser$Browser$Events$onSelfMsg, 0, $elm$browser$Browser$Events$subMap);
var $elm$browser$Browser$Events$subscription = _Platform_leaf('Browser.Events');
var $elm$browser$Browser$Events$on = F3(
	function (node, name, decoder) {
		return $elm$browser$Browser$Events$subscription(
			A3($elm$browser$Browser$Events$MySub, node, name, decoder));
	});
var $elm$browser$Browser$Events$onMouseMove = A2($elm$browser$Browser$Events$on, $elm$browser$Browser$Events$Document, 'mousemove');
var $elm$browser$Browser$Events$onMouseUp = A2($elm$browser$Browser$Events$on, $elm$browser$Browser$Events$Document, 'mouseup');
var $zaboco$elm_draggable$Internal$Position = F2(
	function (x, y) {
		return {x: x, y: y};
	});
var $elm$core$Basics$truncate = _Basics_truncate;
var $zaboco$elm_draggable$Draggable$positionDecoder = A3(
	$elm$json$Json$Decode$map2,
	$zaboco$elm_draggable$Internal$Position,
	A2(
		$elm$json$Json$Decode$map,
		$elm$core$Basics$truncate,
		A2($elm$json$Json$Decode$field, 'pageX', $elm$json$Json$Decode$float)),
	A2(
		$elm$json$Json$Decode$map,
		$elm$core$Basics$truncate,
		A2($elm$json$Json$Decode$field, 'pageY', $elm$json$Json$Decode$float)));
var $zaboco$elm_draggable$Draggable$subscriptions = F2(
	function (envelope, _v0) {
		var drag = _v0.a;
		if (drag.$ === 'NotDragging') {
			return $elm$core$Platform$Sub$none;
		} else {
			return A2(
				$elm$core$Platform$Sub$map,
				A2($elm$core$Basics$composeL, envelope, $zaboco$elm_draggable$Draggable$Msg),
				$elm$core$Platform$Sub$batch(
					_List_fromArray(
						[
							$elm$browser$Browser$Events$onMouseMove(
							A2($elm$json$Json$Decode$map, $zaboco$elm_draggable$Internal$DragAt, $zaboco$elm_draggable$Draggable$positionDecoder)),
							$elm$browser$Browser$Events$onMouseUp(
							$elm$json$Json$Decode$succeed($zaboco$elm_draggable$Internal$StopDragging))
						])));
		}
	});
var $author$project$Canvas$subscriptions = function (model) {
	var drag = model.drag;
	return $elm$core$Platform$Sub$batch(
		_List_fromArray(
			[
				A2($zaboco$elm_draggable$Draggable$subscriptions, $author$project$Canvas$DragMsg, drag)
			]));
};
var $elm_explorations$linear_algebra$Math$Vector2$add = _MJS_v2add;
var $elm$core$Basics$clamp = F3(
	function (low, high, number) {
		return (_Utils_cmp(number, low) < 0) ? low : ((_Utils_cmp(number, high) > 0) ? high : number);
	});
var $author$project$Canvas$OnDragBy = function (a) {
	return {$: 'OnDragBy', a: a};
};
var $zaboco$elm_draggable$Draggable$Config = function (a) {
	return {$: 'Config', a: a};
};
var $zaboco$elm_draggable$Internal$defaultConfig = {
	onClick: function (_v0) {
		return $elm$core$Maybe$Nothing;
	},
	onDragBy: function (_v1) {
		return $elm$core$Maybe$Nothing;
	},
	onDragEnd: $elm$core$Maybe$Nothing,
	onDragStart: function (_v2) {
		return $elm$core$Maybe$Nothing;
	},
	onMouseDown: function (_v3) {
		return $elm$core$Maybe$Nothing;
	}
};
var $zaboco$elm_draggable$Draggable$basicConfig = function (onDragByListener) {
	var defaultConfig = $zaboco$elm_draggable$Internal$defaultConfig;
	return $zaboco$elm_draggable$Draggable$Config(
		_Utils_update(
			defaultConfig,
			{
				onDragBy: A2($elm$core$Basics$composeL, $elm$core$Maybe$Just, onDragByListener)
			}));
};
var $elm_explorations$linear_algebra$Math$Vector2$vec2 = _MJS_v2;
var $author$project$Canvas$dragConfig = $zaboco$elm_draggable$Draggable$basicConfig(
	A2(
		$elm$core$Basics$composeL,
		$author$project$Canvas$OnDragBy,
		function (_v0) {
			var dx = _v0.a;
			var dy = _v0.b;
			return A2($elm_explorations$linear_algebra$Math$Vector2$vec2, dx, dy);
		}));
var $elm$core$Basics$negate = function (n) {
	return -n;
};
var $elm$core$Basics$abs = function (n) {
	return (n < 0) ? (-n) : n;
};
var $elm$core$List$sum = function (numbers) {
	return A3($elm$core$List$foldl, $elm$core$Basics$add, 0, numbers);
};
var $author$project$Canvas$getAutomaticallyNiceScalableFactor = F3(
	function (config, ratio, values) {
		var averageValue = $elm$core$List$sum(
			A2($elm$core$List$map, $elm$core$Basics$abs, values)) / $elm$core$List$length(values);
		var _v0 = config;
		var width = _v0.width;
		var height = _v0.height;
		var margin = _v0.margin;
		var baseLength = A2($elm$core$Basics$min, width - (2.0 * margin), height - (2.0 * margin));
		return (ratio * baseLength) / averageValue;
	});
var $author$project$Canvas$getAutomaticallyNiceMomentLineScalableFactors = F2(
	function (model, scalableFactors) {
		var _v0 = model;
		var config = _v0.config;
		var entities = _v0.entities;
		var getAutomaticallyFactor = A2($author$project$Canvas$getAutomaticallyNiceScalableFactor, config, 0.1);
		var mlines = A2(
			$elm$core$Debug$log,
			'mlines',
			A2(
				$elm$core$List$concatMap,
				function (mline) {
					return _List_fromArray(
						[mline.m0, mline.m1, mline.m2]);
				},
				A2(
					$elm$core$List$concatMap,
					function (layer) {
						return layer.momentLines;
					},
					entities.layers)));
		return function (factors) {
			if (0 < $elm$core$List$length(mlines)) {
				var value = A2(
					$elm$core$Debug$log,
					'momentLine factor',
					getAutomaticallyFactor(mlines));
				return _Utils_update(
					factors,
					{momentLine: value});
			} else {
				return factors;
			}
		}(scalableFactors);
	});
var $author$project$Canvas$getAutomaticallyNiceScalableCircleScalableFactors = F2(
	function (model, scalableFactors) {
		var _v0 = model;
		var config = _v0.config;
		var entities = _v0.entities;
		var getAutomaticallyFactor = A2($author$project$Canvas$getAutomaticallyNiceScalableFactor, config, 0.1);
		var scircles = A2(
			$elm$core$List$map,
			function (scircle) {
				return scircle.value;
			},
			A2(
				$elm$core$List$concatMap,
				function (layer) {
					return layer.scalableCircles;
				},
				entities.layers));
		return function (factors) {
			var value = A2(
				$elm$core$Debug$log,
				'scalableCircle factor',
				getAutomaticallyFactor(scircles));
			return (0 < $elm$core$List$length(scircles)) ? _Utils_update(
				factors,
				{scalableCircle: value}) : factors;
		}(scalableFactors);
	});
var $author$project$Canvas$getAutomaticallyNiceScalableLineScalableFactors = F2(
	function (model, scalableFactors) {
		var _v0 = model;
		var config = _v0.config;
		var entities = _v0.entities;
		var getAutomaticallyFactor = A2($author$project$Canvas$getAutomaticallyNiceScalableFactor, config, 0.1);
		var slines = A2(
			$elm$core$List$concatMap,
			function (sline) {
				return _List_fromArray(
					[sline.dx1, sline.dy1, sline.dx2, sline.dy2]);
			},
			A2(
				$elm$core$List$concatMap,
				function (layer) {
					return layer.scalableLines;
				},
				entities.layers));
		return function (factors) {
			var value = A2(
				$elm$core$Debug$log,
				'scalableLine factor',
				getAutomaticallyFactor(slines));
			return (0 < $elm$core$List$length(slines)) ? _Utils_update(
				factors,
				{scalableLine: value}) : factors;
		}(scalableFactors);
	});
var $author$project$Canvas$getAutomaticallyNiceScalableFactors = function (model) {
	var _v0 = model;
	var config = _v0.config;
	var scalableFactors = config.scalableFactors;
	var processors = (scalableFactors.momentLine === 0.0) ? _List_fromArray(
		[
			$author$project$Canvas$getAutomaticallyNiceMomentLineScalableFactors(model)
		]) : _Utils_ap(
		_List_Nil,
		(scalableFactors.scalableLine === 0.0) ? _List_fromArray(
			[
				$author$project$Canvas$getAutomaticallyNiceScalableLineScalableFactors(model)
			]) : _Utils_ap(
			_List_Nil,
			(scalableFactors.scalableCircle === 0.0) ? _List_fromArray(
				[
					$author$project$Canvas$getAutomaticallyNiceScalableCircleScalableFactors(model)
				]) : _List_Nil));
	var _v1 = A2(
		$elm$core$Debug$log,
		'processors',
		$elm$core$List$length(processors));
	return A3(
		$elm$core$List$foldl,
		F2(
			function (f, factors) {
				return f(factors);
			}),
		scalableFactors,
		processors);
};
var $elm_explorations$linear_algebra$Math$Vector2$getX = _MJS_v2getX;
var $elm_explorations$linear_algebra$Math$Vector2$getY = _MJS_v2getY;
var $author$project$Canvas$magnifiedScalableFactor = F3(
	function (entities, magnify, scalableFactors) {
		var slines = A2(
			$elm$core$List$concatMap,
			function (layer) {
				return layer.scalableLines;
			},
			entities.layers);
		var scircles = A2(
			$elm$core$List$concatMap,
			function (layer) {
				return layer.scalableCircles;
			},
			entities.layers);
		var mlines = A2(
			$elm$core$List$concatMap,
			function (layer) {
				return layer.momentLines;
			},
			entities.layers);
		return function (factors) {
			return (0 < $elm$core$List$length(scircles)) ? _Utils_update(
				factors,
				{scalableCircle: factors.scalableCircle * magnify}) : factors;
		}(
			function (factors) {
				return (0 < $elm$core$List$length(slines)) ? _Utils_update(
					factors,
					{scalableLine: factors.scalableLine * magnify}) : factors;
			}(
				function (factors) {
					return (0 < $elm$core$List$length(mlines)) ? _Utils_update(
						factors,
						{momentLine: factors.momentLine * magnify}) : factors;
				}(scalableFactors)));
	});
var $author$project$Canvas$ResponseEntities = function (a) {
	return {$: 'ResponseEntities', a: a};
};
var $elm$json$Json$Decode$decodeString = _Json_runOnString;
var $elm$http$Http$BadStatus_ = F2(
	function (a, b) {
		return {$: 'BadStatus_', a: a, b: b};
	});
var $elm$http$Http$BadUrl_ = function (a) {
	return {$: 'BadUrl_', a: a};
};
var $elm$http$Http$GoodStatus_ = F2(
	function (a, b) {
		return {$: 'GoodStatus_', a: a, b: b};
	});
var $elm$http$Http$NetworkError_ = {$: 'NetworkError_'};
var $elm$http$Http$Receiving = function (a) {
	return {$: 'Receiving', a: a};
};
var $elm$http$Http$Sending = function (a) {
	return {$: 'Sending', a: a};
};
var $elm$http$Http$Timeout_ = {$: 'Timeout_'};
var $elm$core$Maybe$isJust = function (maybe) {
	if (maybe.$ === 'Just') {
		return true;
	} else {
		return false;
	}
};
var $elm$core$Dict$get = F2(
	function (targetKey, dict) {
		get:
		while (true) {
			if (dict.$ === 'RBEmpty_elm_builtin') {
				return $elm$core$Maybe$Nothing;
			} else {
				var key = dict.b;
				var value = dict.c;
				var left = dict.d;
				var right = dict.e;
				var _v1 = A2($elm$core$Basics$compare, targetKey, key);
				switch (_v1.$) {
					case 'LT':
						var $temp$targetKey = targetKey,
							$temp$dict = left;
						targetKey = $temp$targetKey;
						dict = $temp$dict;
						continue get;
					case 'EQ':
						return $elm$core$Maybe$Just(value);
					default:
						var $temp$targetKey = targetKey,
							$temp$dict = right;
						targetKey = $temp$targetKey;
						dict = $temp$dict;
						continue get;
				}
			}
		}
	});
var $elm$core$Dict$getMin = function (dict) {
	getMin:
	while (true) {
		if ((dict.$ === 'RBNode_elm_builtin') && (dict.d.$ === 'RBNode_elm_builtin')) {
			var left = dict.d;
			var $temp$dict = left;
			dict = $temp$dict;
			continue getMin;
		} else {
			return dict;
		}
	}
};
var $elm$core$Dict$moveRedLeft = function (dict) {
	if (((dict.$ === 'RBNode_elm_builtin') && (dict.d.$ === 'RBNode_elm_builtin')) && (dict.e.$ === 'RBNode_elm_builtin')) {
		if ((dict.e.d.$ === 'RBNode_elm_builtin') && (dict.e.d.a.$ === 'Red')) {
			var clr = dict.a;
			var k = dict.b;
			var v = dict.c;
			var _v1 = dict.d;
			var lClr = _v1.a;
			var lK = _v1.b;
			var lV = _v1.c;
			var lLeft = _v1.d;
			var lRight = _v1.e;
			var _v2 = dict.e;
			var rClr = _v2.a;
			var rK = _v2.b;
			var rV = _v2.c;
			var rLeft = _v2.d;
			var _v3 = rLeft.a;
			var rlK = rLeft.b;
			var rlV = rLeft.c;
			var rlL = rLeft.d;
			var rlR = rLeft.e;
			var rRight = _v2.e;
			return A5(
				$elm$core$Dict$RBNode_elm_builtin,
				$elm$core$Dict$Red,
				rlK,
				rlV,
				A5(
					$elm$core$Dict$RBNode_elm_builtin,
					$elm$core$Dict$Black,
					k,
					v,
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, lK, lV, lLeft, lRight),
					rlL),
				A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Black, rK, rV, rlR, rRight));
		} else {
			var clr = dict.a;
			var k = dict.b;
			var v = dict.c;
			var _v4 = dict.d;
			var lClr = _v4.a;
			var lK = _v4.b;
			var lV = _v4.c;
			var lLeft = _v4.d;
			var lRight = _v4.e;
			var _v5 = dict.e;
			var rClr = _v5.a;
			var rK = _v5.b;
			var rV = _v5.c;
			var rLeft = _v5.d;
			var rRight = _v5.e;
			if (clr.$ === 'Black') {
				return A5(
					$elm$core$Dict$RBNode_elm_builtin,
					$elm$core$Dict$Black,
					k,
					v,
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, lK, lV, lLeft, lRight),
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, rK, rV, rLeft, rRight));
			} else {
				return A5(
					$elm$core$Dict$RBNode_elm_builtin,
					$elm$core$Dict$Black,
					k,
					v,
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, lK, lV, lLeft, lRight),
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, rK, rV, rLeft, rRight));
			}
		}
	} else {
		return dict;
	}
};
var $elm$core$Dict$moveRedRight = function (dict) {
	if (((dict.$ === 'RBNode_elm_builtin') && (dict.d.$ === 'RBNode_elm_builtin')) && (dict.e.$ === 'RBNode_elm_builtin')) {
		if ((dict.d.d.$ === 'RBNode_elm_builtin') && (dict.d.d.a.$ === 'Red')) {
			var clr = dict.a;
			var k = dict.b;
			var v = dict.c;
			var _v1 = dict.d;
			var lClr = _v1.a;
			var lK = _v1.b;
			var lV = _v1.c;
			var _v2 = _v1.d;
			var _v3 = _v2.a;
			var llK = _v2.b;
			var llV = _v2.c;
			var llLeft = _v2.d;
			var llRight = _v2.e;
			var lRight = _v1.e;
			var _v4 = dict.e;
			var rClr = _v4.a;
			var rK = _v4.b;
			var rV = _v4.c;
			var rLeft = _v4.d;
			var rRight = _v4.e;
			return A5(
				$elm$core$Dict$RBNode_elm_builtin,
				$elm$core$Dict$Red,
				lK,
				lV,
				A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Black, llK, llV, llLeft, llRight),
				A5(
					$elm$core$Dict$RBNode_elm_builtin,
					$elm$core$Dict$Black,
					k,
					v,
					lRight,
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, rK, rV, rLeft, rRight)));
		} else {
			var clr = dict.a;
			var k = dict.b;
			var v = dict.c;
			var _v5 = dict.d;
			var lClr = _v5.a;
			var lK = _v5.b;
			var lV = _v5.c;
			var lLeft = _v5.d;
			var lRight = _v5.e;
			var _v6 = dict.e;
			var rClr = _v6.a;
			var rK = _v6.b;
			var rV = _v6.c;
			var rLeft = _v6.d;
			var rRight = _v6.e;
			if (clr.$ === 'Black') {
				return A5(
					$elm$core$Dict$RBNode_elm_builtin,
					$elm$core$Dict$Black,
					k,
					v,
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, lK, lV, lLeft, lRight),
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, rK, rV, rLeft, rRight));
			} else {
				return A5(
					$elm$core$Dict$RBNode_elm_builtin,
					$elm$core$Dict$Black,
					k,
					v,
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, lK, lV, lLeft, lRight),
					A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, rK, rV, rLeft, rRight));
			}
		}
	} else {
		return dict;
	}
};
var $elm$core$Dict$removeHelpPrepEQGT = F7(
	function (targetKey, dict, color, key, value, left, right) {
		if ((left.$ === 'RBNode_elm_builtin') && (left.a.$ === 'Red')) {
			var _v1 = left.a;
			var lK = left.b;
			var lV = left.c;
			var lLeft = left.d;
			var lRight = left.e;
			return A5(
				$elm$core$Dict$RBNode_elm_builtin,
				color,
				lK,
				lV,
				lLeft,
				A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Red, key, value, lRight, right));
		} else {
			_v2$2:
			while (true) {
				if ((right.$ === 'RBNode_elm_builtin') && (right.a.$ === 'Black')) {
					if (right.d.$ === 'RBNode_elm_builtin') {
						if (right.d.a.$ === 'Black') {
							var _v3 = right.a;
							var _v4 = right.d;
							var _v5 = _v4.a;
							return $elm$core$Dict$moveRedRight(dict);
						} else {
							break _v2$2;
						}
					} else {
						var _v6 = right.a;
						var _v7 = right.d;
						return $elm$core$Dict$moveRedRight(dict);
					}
				} else {
					break _v2$2;
				}
			}
			return dict;
		}
	});
var $elm$core$Dict$removeMin = function (dict) {
	if ((dict.$ === 'RBNode_elm_builtin') && (dict.d.$ === 'RBNode_elm_builtin')) {
		var color = dict.a;
		var key = dict.b;
		var value = dict.c;
		var left = dict.d;
		var lColor = left.a;
		var lLeft = left.d;
		var right = dict.e;
		if (lColor.$ === 'Black') {
			if ((lLeft.$ === 'RBNode_elm_builtin') && (lLeft.a.$ === 'Red')) {
				var _v3 = lLeft.a;
				return A5(
					$elm$core$Dict$RBNode_elm_builtin,
					color,
					key,
					value,
					$elm$core$Dict$removeMin(left),
					right);
			} else {
				var _v4 = $elm$core$Dict$moveRedLeft(dict);
				if (_v4.$ === 'RBNode_elm_builtin') {
					var nColor = _v4.a;
					var nKey = _v4.b;
					var nValue = _v4.c;
					var nLeft = _v4.d;
					var nRight = _v4.e;
					return A5(
						$elm$core$Dict$balance,
						nColor,
						nKey,
						nValue,
						$elm$core$Dict$removeMin(nLeft),
						nRight);
				} else {
					return $elm$core$Dict$RBEmpty_elm_builtin;
				}
			}
		} else {
			return A5(
				$elm$core$Dict$RBNode_elm_builtin,
				color,
				key,
				value,
				$elm$core$Dict$removeMin(left),
				right);
		}
	} else {
		return $elm$core$Dict$RBEmpty_elm_builtin;
	}
};
var $elm$core$Dict$removeHelp = F2(
	function (targetKey, dict) {
		if (dict.$ === 'RBEmpty_elm_builtin') {
			return $elm$core$Dict$RBEmpty_elm_builtin;
		} else {
			var color = dict.a;
			var key = dict.b;
			var value = dict.c;
			var left = dict.d;
			var right = dict.e;
			if (_Utils_cmp(targetKey, key) < 0) {
				if ((left.$ === 'RBNode_elm_builtin') && (left.a.$ === 'Black')) {
					var _v4 = left.a;
					var lLeft = left.d;
					if ((lLeft.$ === 'RBNode_elm_builtin') && (lLeft.a.$ === 'Red')) {
						var _v6 = lLeft.a;
						return A5(
							$elm$core$Dict$RBNode_elm_builtin,
							color,
							key,
							value,
							A2($elm$core$Dict$removeHelp, targetKey, left),
							right);
					} else {
						var _v7 = $elm$core$Dict$moveRedLeft(dict);
						if (_v7.$ === 'RBNode_elm_builtin') {
							var nColor = _v7.a;
							var nKey = _v7.b;
							var nValue = _v7.c;
							var nLeft = _v7.d;
							var nRight = _v7.e;
							return A5(
								$elm$core$Dict$balance,
								nColor,
								nKey,
								nValue,
								A2($elm$core$Dict$removeHelp, targetKey, nLeft),
								nRight);
						} else {
							return $elm$core$Dict$RBEmpty_elm_builtin;
						}
					}
				} else {
					return A5(
						$elm$core$Dict$RBNode_elm_builtin,
						color,
						key,
						value,
						A2($elm$core$Dict$removeHelp, targetKey, left),
						right);
				}
			} else {
				return A2(
					$elm$core$Dict$removeHelpEQGT,
					targetKey,
					A7($elm$core$Dict$removeHelpPrepEQGT, targetKey, dict, color, key, value, left, right));
			}
		}
	});
var $elm$core$Dict$removeHelpEQGT = F2(
	function (targetKey, dict) {
		if (dict.$ === 'RBNode_elm_builtin') {
			var color = dict.a;
			var key = dict.b;
			var value = dict.c;
			var left = dict.d;
			var right = dict.e;
			if (_Utils_eq(targetKey, key)) {
				var _v1 = $elm$core$Dict$getMin(right);
				if (_v1.$ === 'RBNode_elm_builtin') {
					var minKey = _v1.b;
					var minValue = _v1.c;
					return A5(
						$elm$core$Dict$balance,
						color,
						minKey,
						minValue,
						left,
						$elm$core$Dict$removeMin(right));
				} else {
					return $elm$core$Dict$RBEmpty_elm_builtin;
				}
			} else {
				return A5(
					$elm$core$Dict$balance,
					color,
					key,
					value,
					left,
					A2($elm$core$Dict$removeHelp, targetKey, right));
			}
		} else {
			return $elm$core$Dict$RBEmpty_elm_builtin;
		}
	});
var $elm$core$Dict$remove = F2(
	function (key, dict) {
		var _v0 = A2($elm$core$Dict$removeHelp, key, dict);
		if ((_v0.$ === 'RBNode_elm_builtin') && (_v0.a.$ === 'Red')) {
			var _v1 = _v0.a;
			var k = _v0.b;
			var v = _v0.c;
			var l = _v0.d;
			var r = _v0.e;
			return A5($elm$core$Dict$RBNode_elm_builtin, $elm$core$Dict$Black, k, v, l, r);
		} else {
			var x = _v0;
			return x;
		}
	});
var $elm$core$Dict$update = F3(
	function (targetKey, alter, dictionary) {
		var _v0 = alter(
			A2($elm$core$Dict$get, targetKey, dictionary));
		if (_v0.$ === 'Just') {
			var value = _v0.a;
			return A3($elm$core$Dict$insert, targetKey, value, dictionary);
		} else {
			return A2($elm$core$Dict$remove, targetKey, dictionary);
		}
	});
var $elm$core$Basics$composeR = F3(
	function (f, g, x) {
		return g(
			f(x));
	});
var $elm$http$Http$expectStringResponse = F2(
	function (toMsg, toResult) {
		return A3(
			_Http_expect,
			'',
			$elm$core$Basics$identity,
			A2($elm$core$Basics$composeR, toResult, toMsg));
	});
var $elm$core$Result$mapError = F2(
	function (f, result) {
		if (result.$ === 'Ok') {
			var v = result.a;
			return $elm$core$Result$Ok(v);
		} else {
			var e = result.a;
			return $elm$core$Result$Err(
				f(e));
		}
	});
var $elm$http$Http$BadBody = function (a) {
	return {$: 'BadBody', a: a};
};
var $elm$http$Http$BadStatus = function (a) {
	return {$: 'BadStatus', a: a};
};
var $elm$http$Http$BadUrl = function (a) {
	return {$: 'BadUrl', a: a};
};
var $elm$http$Http$NetworkError = {$: 'NetworkError'};
var $elm$http$Http$Timeout = {$: 'Timeout'};
var $elm$http$Http$resolve = F2(
	function (toResult, response) {
		switch (response.$) {
			case 'BadUrl_':
				var url = response.a;
				return $elm$core$Result$Err(
					$elm$http$Http$BadUrl(url));
			case 'Timeout_':
				return $elm$core$Result$Err($elm$http$Http$Timeout);
			case 'NetworkError_':
				return $elm$core$Result$Err($elm$http$Http$NetworkError);
			case 'BadStatus_':
				var metadata = response.a;
				return $elm$core$Result$Err(
					$elm$http$Http$BadStatus(metadata.statusCode));
			default:
				var body = response.b;
				return A2(
					$elm$core$Result$mapError,
					$elm$http$Http$BadBody,
					toResult(body));
		}
	});
var $elm$http$Http$expectJson = F2(
	function (toMsg, decoder) {
		return A2(
			$elm$http$Http$expectStringResponse,
			toMsg,
			$elm$http$Http$resolve(
				function (string) {
					return A2(
						$elm$core$Result$mapError,
						$elm$json$Json$Decode$errorToString,
						A2($elm$json$Json$Decode$decodeString, decoder, string));
				}));
	});
var $elm$http$Http$emptyBody = _Http_emptyBody;
var $elm$http$Http$Request = function (a) {
	return {$: 'Request', a: a};
};
var $elm$http$Http$State = F2(
	function (reqs, subs) {
		return {reqs: reqs, subs: subs};
	});
var $elm$http$Http$init = $elm$core$Task$succeed(
	A2($elm$http$Http$State, $elm$core$Dict$empty, _List_Nil));
var $elm$core$Process$spawn = _Scheduler_spawn;
var $elm$http$Http$updateReqs = F3(
	function (router, cmds, reqs) {
		updateReqs:
		while (true) {
			if (!cmds.b) {
				return $elm$core$Task$succeed(reqs);
			} else {
				var cmd = cmds.a;
				var otherCmds = cmds.b;
				if (cmd.$ === 'Cancel') {
					var tracker = cmd.a;
					var _v2 = A2($elm$core$Dict$get, tracker, reqs);
					if (_v2.$ === 'Nothing') {
						var $temp$router = router,
							$temp$cmds = otherCmds,
							$temp$reqs = reqs;
						router = $temp$router;
						cmds = $temp$cmds;
						reqs = $temp$reqs;
						continue updateReqs;
					} else {
						var pid = _v2.a;
						return A2(
							$elm$core$Task$andThen,
							function (_v3) {
								return A3(
									$elm$http$Http$updateReqs,
									router,
									otherCmds,
									A2($elm$core$Dict$remove, tracker, reqs));
							},
							$elm$core$Process$kill(pid));
					}
				} else {
					var req = cmd.a;
					return A2(
						$elm$core$Task$andThen,
						function (pid) {
							var _v4 = req.tracker;
							if (_v4.$ === 'Nothing') {
								return A3($elm$http$Http$updateReqs, router, otherCmds, reqs);
							} else {
								var tracker = _v4.a;
								return A3(
									$elm$http$Http$updateReqs,
									router,
									otherCmds,
									A3($elm$core$Dict$insert, tracker, pid, reqs));
							}
						},
						$elm$core$Process$spawn(
							A3(
								_Http_toTask,
								router,
								$elm$core$Platform$sendToApp(router),
								req)));
				}
			}
		}
	});
var $elm$http$Http$onEffects = F4(
	function (router, cmds, subs, state) {
		return A2(
			$elm$core$Task$andThen,
			function (reqs) {
				return $elm$core$Task$succeed(
					A2($elm$http$Http$State, reqs, subs));
			},
			A3($elm$http$Http$updateReqs, router, cmds, state.reqs));
	});
var $elm$http$Http$maybeSend = F4(
	function (router, desiredTracker, progress, _v0) {
		var actualTracker = _v0.a;
		var toMsg = _v0.b;
		return _Utils_eq(desiredTracker, actualTracker) ? $elm$core$Maybe$Just(
			A2(
				$elm$core$Platform$sendToApp,
				router,
				toMsg(progress))) : $elm$core$Maybe$Nothing;
	});
var $elm$http$Http$onSelfMsg = F3(
	function (router, _v0, state) {
		var tracker = _v0.a;
		var progress = _v0.b;
		return A2(
			$elm$core$Task$andThen,
			function (_v1) {
				return $elm$core$Task$succeed(state);
			},
			$elm$core$Task$sequence(
				A2(
					$elm$core$List$filterMap,
					A3($elm$http$Http$maybeSend, router, tracker, progress),
					state.subs)));
	});
var $elm$http$Http$Cancel = function (a) {
	return {$: 'Cancel', a: a};
};
var $elm$http$Http$cmdMap = F2(
	function (func, cmd) {
		if (cmd.$ === 'Cancel') {
			var tracker = cmd.a;
			return $elm$http$Http$Cancel(tracker);
		} else {
			var r = cmd.a;
			return $elm$http$Http$Request(
				{
					allowCookiesFromOtherDomains: r.allowCookiesFromOtherDomains,
					body: r.body,
					expect: A2(_Http_mapExpect, func, r.expect),
					headers: r.headers,
					method: r.method,
					timeout: r.timeout,
					tracker: r.tracker,
					url: r.url
				});
		}
	});
var $elm$http$Http$MySub = F2(
	function (a, b) {
		return {$: 'MySub', a: a, b: b};
	});
var $elm$http$Http$subMap = F2(
	function (func, _v0) {
		var tracker = _v0.a;
		var toMsg = _v0.b;
		return A2(
			$elm$http$Http$MySub,
			tracker,
			A2($elm$core$Basics$composeR, toMsg, func));
	});
_Platform_effectManagers['Http'] = _Platform_createManager($elm$http$Http$init, $elm$http$Http$onEffects, $elm$http$Http$onSelfMsg, $elm$http$Http$cmdMap, $elm$http$Http$subMap);
var $elm$http$Http$command = _Platform_leaf('Http');
var $elm$http$Http$subscription = _Platform_leaf('Http');
var $elm$http$Http$request = function (r) {
	return $elm$http$Http$command(
		$elm$http$Http$Request(
			{allowCookiesFromOtherDomains: false, body: r.body, expect: r.expect, headers: r.headers, method: r.method, timeout: r.timeout, tracker: r.tracker, url: r.url}));
};
var $elm$http$Http$get = function (r) {
	return $elm$http$Http$request(
		{body: $elm$http$Http$emptyBody, expect: r.expect, headers: _List_Nil, method: 'GET', timeout: $elm$core$Maybe$Nothing, tracker: $elm$core$Maybe$Nothing, url: r.url});
};
var $author$project$Canvas$requestEntities = function (url) {
	return $elm$http$Http$get(
		{
			expect: A2($elm$http$Http$expectJson, $author$project$Canvas$ResponseEntities, $author$project$Canvas$decodeEntities),
			url: url
		});
};
var $elm_explorations$linear_algebra$Math$Vector2$scale = _MJS_v2scale;
var $elm$core$Maybe$map = F2(
	function (f, maybe) {
		if (maybe.$ === 'Just') {
			var value = maybe.a;
			return $elm$core$Maybe$Just(
				f(value));
		} else {
			return $elm$core$Maybe$Nothing;
		}
	});
var $zaboco$elm_draggable$Cmd$Extra$message = function (x) {
	return A2(
		$elm$core$Task$perform,
		$elm$core$Basics$identity,
		$elm$core$Task$succeed(x));
};
var $zaboco$elm_draggable$Cmd$Extra$optionalMessage = function (msgMaybe) {
	return A2(
		$elm$core$Maybe$withDefault,
		$elm$core$Platform$Cmd$none,
		A2($elm$core$Maybe$map, $zaboco$elm_draggable$Cmd$Extra$message, msgMaybe));
};
var $zaboco$elm_draggable$Internal$Dragging = function (a) {
	return {$: 'Dragging', a: a};
};
var $zaboco$elm_draggable$Internal$DraggingTentative = F2(
	function (a, b) {
		return {$: 'DraggingTentative', a: a, b: b};
	});
var $zaboco$elm_draggable$Internal$distanceTo = F2(
	function (end, start) {
		return _Utils_Tuple2(end.x - start.x, end.y - start.y);
	});
var $zaboco$elm_draggable$Internal$updateAndEmit = F3(
	function (config, msg, drag) {
		var _v0 = _Utils_Tuple2(drag, msg);
		_v0$5:
		while (true) {
			switch (_v0.a.$) {
				case 'NotDragging':
					if (_v0.b.$ === 'StartDragging') {
						var _v1 = _v0.a;
						var _v2 = _v0.b;
						var key = _v2.a;
						var initialPosition = _v2.b;
						return _Utils_Tuple2(
							A2($zaboco$elm_draggable$Internal$DraggingTentative, key, initialPosition),
							config.onMouseDown(key));
					} else {
						break _v0$5;
					}
				case 'DraggingTentative':
					switch (_v0.b.$) {
						case 'DragAt':
							var _v3 = _v0.a;
							var key = _v3.a;
							var oldPosition = _v3.b;
							return _Utils_Tuple2(
								$zaboco$elm_draggable$Internal$Dragging(oldPosition),
								config.onDragStart(key));
						case 'StopDragging':
							var _v4 = _v0.a;
							var key = _v4.a;
							var _v5 = _v0.b;
							return _Utils_Tuple2(
								$zaboco$elm_draggable$Internal$NotDragging,
								config.onClick(key));
						default:
							break _v0$5;
					}
				default:
					switch (_v0.b.$) {
						case 'DragAt':
							var oldPosition = _v0.a.a;
							var newPosition = _v0.b.a;
							return _Utils_Tuple2(
								$zaboco$elm_draggable$Internal$Dragging(newPosition),
								config.onDragBy(
									A2($zaboco$elm_draggable$Internal$distanceTo, newPosition, oldPosition)));
						case 'StopDragging':
							var _v6 = _v0.b;
							return _Utils_Tuple2($zaboco$elm_draggable$Internal$NotDragging, config.onDragEnd);
						default:
							break _v0$5;
					}
			}
		}
		return _Utils_Tuple2(drag, $elm$core$Maybe$Nothing);
	});
var $zaboco$elm_draggable$Draggable$updateDraggable = F3(
	function (_v0, _v1, _v2) {
		var config = _v0.a;
		var msg = _v1.a;
		var drag = _v2.a;
		var _v3 = A3($zaboco$elm_draggable$Internal$updateAndEmit, config, msg, drag);
		var newDrag = _v3.a;
		var newMsgMaybe = _v3.b;
		return _Utils_Tuple2(
			$zaboco$elm_draggable$Draggable$State(newDrag),
			$zaboco$elm_draggable$Cmd$Extra$optionalMessage(newMsgMaybe));
	});
var $zaboco$elm_draggable$Draggable$update = F3(
	function (config, msg, model) {
		var _v0 = A3($zaboco$elm_draggable$Draggable$updateDraggable, config, msg, model.drag);
		var dragState = _v0.a;
		var dragCmd = _v0.b;
		return _Utils_Tuple2(
			_Utils_update(
				model,
				{drag: dragState}),
			dragCmd);
	});
var $author$project$Canvas$update = F2(
	function (msg, model) {
		var entities = model.entities;
		var config = model.config;
		var zoom = config.zoom;
		var center = A2($elm_explorations$linear_algebra$Math$Vector2$vec2, config.centerX, config.centerY);
		switch (msg.$) {
			case 'OnDragBy':
				var rawDelta = msg.a;
				var delta = A2($elm_explorations$linear_algebra$Math$Vector2$scale, (-1) / zoom, rawDelta);
				var newCenter = A2($elm_explorations$linear_algebra$Math$Vector2$add, delta, center);
				return _Utils_Tuple2(
					_Utils_update(
						model,
						{
							config: _Utils_update(
								config,
								{
									centerX: $elm_explorations$linear_algebra$Math$Vector2$getX(newCenter),
									centerY: $elm_explorations$linear_algebra$Math$Vector2$getY(newCenter)
								})
						}),
					$elm$core$Platform$Cmd$none);
			case 'Zoom':
				var factor = msg.a;
				var newZoom = A3($elm$core$Basics$clamp, 0.01, 100, (factor * 0.01) + zoom);
				return _Utils_Tuple2(
					_Utils_update(
						model,
						{
							config: _Utils_update(
								config,
								{zoom: newZoom})
						}),
					$elm$core$Platform$Cmd$none);
			case 'ResetInitialState':
				return _Utils_Tuple2(
					_Utils_update(
						model,
						{config: model.initialConfig}),
					$elm$core$Platform$Cmd$none);
			case 'DragMsg':
				var dragMsg = msg.a;
				return A3($zaboco$elm_draggable$Draggable$update, $author$project$Canvas$dragConfig, dragMsg, model);
			case 'UpdateFontSize':
				var value = msg.a;
				var newConfig = _Utils_update(
					config,
					{fontSize: config.fontSize + value});
				return _Utils_Tuple2(
					_Utils_update(
						model,
						{config: newConfig}),
					$elm$core$Platform$Cmd$none);
			case 'ScalableFactorUp':
				var scalableFactors = config.scalableFactors;
				var newScalableFactors = A3($author$project$Canvas$magnifiedScalableFactor, model.entities, 1.1, scalableFactors);
				var newConfig = A2(
					$elm$core$Debug$log,
					'ScaleUp',
					_Utils_update(
						config,
						{scalableFactors: newScalableFactors}));
				return _Utils_Tuple2(
					_Utils_update(
						model,
						{config: newConfig}),
					$elm$core$Platform$Cmd$none);
			case 'ScalableFactorDown':
				var scalableFactors = config.scalableFactors;
				var newScalableFactors = A3($author$project$Canvas$magnifiedScalableFactor, model.entities, 0.9, scalableFactors);
				var newConfig = A2(
					$elm$core$Debug$log,
					'ScaleDown',
					_Utils_update(
						config,
						{scalableFactors: newScalableFactors}));
				return _Utils_Tuple2(
					_Utils_update(
						model,
						{config: newConfig}),
					$elm$core$Platform$Cmd$none);
			case 'ActivatedTag':
				var tagKey = msg.a;
				return _Utils_Tuple2(
					_Utils_update(
						model,
						{
							tags: A2(
								$elm$core$List$map,
								function (tag) {
									return _Utils_eq(tag.key, tagKey) ? _Utils_update(
										tag,
										{activated: true}) : tag;
								},
								model.tags)
						}),
					$elm$core$Platform$Cmd$none);
			case 'DeactivatedTag':
				var tagKey = msg.a;
				return _Utils_Tuple2(
					_Utils_update(
						model,
						{
							tags: A2(
								$elm$core$List$map,
								function (tag) {
									return _Utils_eq(tag.key, tagKey) ? _Utils_update(
										tag,
										{activated: false}) : tag;
								},
								model.tags)
						}),
					$elm$core$Platform$Cmd$none);
			case 'RequestEntities':
				var url = msg.a;
				return _Utils_Tuple2(
					model,
					$author$project$Canvas$requestEntities(url));
			default:
				var result = msg.a;
				if (result.$ === 'Ok') {
					var response = result.a;
					var converter = $author$project$Canvas$getCoordinateConverter(
						_Utils_update(
							model,
							{entities: response}));
					var newEntities = A2($author$project$Canvas$coordinateConvertEntities, converter, response);
					var newModel = _Utils_update(
						model,
						{entities: newEntities});
					var scalableFactors = A2(
						$elm$core$Debug$log,
						'auto scalableFactors',
						$author$project$Canvas$getAutomaticallyNiceScalableFactors(newModel));
					var newConfig = _Utils_update(
						config,
						{scalableFactors: scalableFactors});
					return _Utils_Tuple2(
						_Utils_update(
							newModel,
							{config: newConfig}),
						$elm$core$Platform$Cmd$none);
				} else {
					var err = result.a;
					var _v2 = A2($elm$core$Debug$log, 'response error', err);
					return _Utils_Tuple2(model, $elm$core$Platform$Cmd$none);
				}
		}
	});
var $author$project$Canvas$Zoom = function (a) {
	return {$: 'Zoom', a: a};
};
var $elm$virtual_dom$VirtualDom$attribute = F2(
	function (key, value) {
		return A2(
			_VirtualDom_attribute,
			_VirtualDom_noOnOrFormAction(key),
			_VirtualDom_noJavaScriptOrHtmlUri(value));
	});
var $elm$html$Html$Attributes$attribute = $elm$virtual_dom$VirtualDom$attribute;
var $elm$svg$Svg$Attributes$fill = _VirtualDom_attribute('fill');
var $elm$svg$Svg$Attributes$height = _VirtualDom_attribute('height');
var $elm$svg$Svg$trustedNode = _VirtualDom_nodeNS('http://www.w3.org/2000/svg');
var $elm$svg$Svg$rect = $elm$svg$Svg$trustedNode('rect');
var $elm$svg$Svg$Attributes$stroke = _VirtualDom_attribute('stroke');
var $elm$svg$Svg$Attributes$width = _VirtualDom_attribute('width');
var $elm$svg$Svg$Attributes$x = _VirtualDom_attribute('x');
var $elm$svg$Svg$Attributes$y = _VirtualDom_attribute('y');
var $author$project$Canvas$background = A2(
	$elm$svg$Svg$rect,
	_List_fromArray(
		[
			$elm$svg$Svg$Attributes$x('0'),
			$elm$svg$Svg$Attributes$y('0'),
			$elm$svg$Svg$Attributes$width('100%'),
			$elm$svg$Svg$Attributes$height('100%'),
			$elm$svg$Svg$Attributes$fill('#ffffff'),
			$elm$svg$Svg$Attributes$stroke('#2A2A2A')
		]),
	_List_Nil);
var $elm$json$Json$Encode$string = _Json_wrap;
var $elm$html$Html$Attributes$stringProperty = F2(
	function (key, string) {
		return A2(
			_VirtualDom_property,
			key,
			$elm$json$Json$Encode$string(string));
	});
var $elm$html$Html$Attributes$class = $elm$html$Html$Attributes$stringProperty('className');
var $elm$html$Html$div = _VirtualDom_node('div');
var $elm$svg$Svg$Attributes$dominantBaseline = _VirtualDom_attribute('dominant-baseline');
var $elm$svg$Svg$circle = $elm$svg$Svg$trustedNode('circle');
var $elm$svg$Svg$Attributes$cx = _VirtualDom_attribute('cx');
var $elm$svg$Svg$Attributes$cy = _VirtualDom_attribute('cy');
var $elm$core$String$fromFloat = _String_fromNumber;
var $author$project$Canvas$num = F2(
	function (attr, value) {
		return attr(
			$elm$core$String$fromFloat(value));
	});
var $elm$svg$Svg$Attributes$opacity = _VirtualDom_attribute('opacity');
var $elm$svg$Svg$Attributes$r = _VirtualDom_attribute('r');
var $elm$svg$Svg$Attributes$strokeWidth = _VirtualDom_attribute('stroke-width');
var $author$project$Canvas$drawCircle = function (circle) {
	return _List_fromArray(
		[
			A2(
			$elm$svg$Svg$circle,
			_List_fromArray(
				[
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$cx, circle.cx),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$cy, circle.cy),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$r, circle.radius),
					$elm$svg$Svg$Attributes$stroke(circle.style.stroke),
					$elm$svg$Svg$Attributes$fill(circle.style.fill),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$opacity, circle.style.opacity),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$strokeWidth, circle.style.strokeWidth)
				]),
			_List_Nil)
		]);
};
var $elm$core$List$filter = F2(
	function (isGood, list) {
		return A3(
			$elm$core$List$foldr,
			F2(
				function (x, xs) {
					return isGood(x) ? A2($elm$core$List$cons, x, xs) : xs;
				}),
			_List_Nil,
			list);
	});
var $elm$core$List$takeReverse = F3(
	function (n, list, kept) {
		takeReverse:
		while (true) {
			if (n <= 0) {
				return kept;
			} else {
				if (!list.b) {
					return kept;
				} else {
					var x = list.a;
					var xs = list.b;
					var $temp$n = n - 1,
						$temp$list = xs,
						$temp$kept = A2($elm$core$List$cons, x, kept);
					n = $temp$n;
					list = $temp$list;
					kept = $temp$kept;
					continue takeReverse;
				}
			}
		}
	});
var $elm$core$List$takeTailRec = F2(
	function (n, list) {
		return $elm$core$List$reverse(
			A3($elm$core$List$takeReverse, n, list, _List_Nil));
	});
var $elm$core$List$takeFast = F3(
	function (ctr, n, list) {
		if (n <= 0) {
			return _List_Nil;
		} else {
			var _v0 = _Utils_Tuple2(n, list);
			_v0$1:
			while (true) {
				_v0$5:
				while (true) {
					if (!_v0.b.b) {
						return list;
					} else {
						if (_v0.b.b.b) {
							switch (_v0.a) {
								case 1:
									break _v0$1;
								case 2:
									var _v2 = _v0.b;
									var x = _v2.a;
									var _v3 = _v2.b;
									var y = _v3.a;
									return _List_fromArray(
										[x, y]);
								case 3:
									if (_v0.b.b.b.b) {
										var _v4 = _v0.b;
										var x = _v4.a;
										var _v5 = _v4.b;
										var y = _v5.a;
										var _v6 = _v5.b;
										var z = _v6.a;
										return _List_fromArray(
											[x, y, z]);
									} else {
										break _v0$5;
									}
								default:
									if (_v0.b.b.b.b && _v0.b.b.b.b.b) {
										var _v7 = _v0.b;
										var x = _v7.a;
										var _v8 = _v7.b;
										var y = _v8.a;
										var _v9 = _v8.b;
										var z = _v9.a;
										var _v10 = _v9.b;
										var w = _v10.a;
										var tl = _v10.b;
										return (ctr > 1000) ? A2(
											$elm$core$List$cons,
											x,
											A2(
												$elm$core$List$cons,
												y,
												A2(
													$elm$core$List$cons,
													z,
													A2(
														$elm$core$List$cons,
														w,
														A2($elm$core$List$takeTailRec, n - 4, tl))))) : A2(
											$elm$core$List$cons,
											x,
											A2(
												$elm$core$List$cons,
												y,
												A2(
													$elm$core$List$cons,
													z,
													A2(
														$elm$core$List$cons,
														w,
														A3($elm$core$List$takeFast, ctr + 1, n - 4, tl)))));
									} else {
										break _v0$5;
									}
							}
						} else {
							if (_v0.a === 1) {
								break _v0$1;
							} else {
								break _v0$5;
							}
						}
					}
				}
				return list;
			}
			var _v1 = _v0.b;
			var x = _v1.a;
			return _List_fromArray(
				[x]);
		}
	});
var $elm$core$List$take = F2(
	function (n, list) {
		return A3($elm$core$List$takeFast, 0, n, list);
	});
var $author$project$Canvas$turboColormapData = _List_fromArray(
	[
		_Utils_Tuple3(0.18995, 0.07176, 0.23217),
		_Utils_Tuple3(0.19483, 0.08339, 0.26149),
		_Utils_Tuple3(0.19956, 0.09498, 0.29024),
		_Utils_Tuple3(0.20415, 0.10652, 0.31844),
		_Utils_Tuple3(0.20860, 0.11802, 0.34607),
		_Utils_Tuple3(0.21291, 0.12947, 0.37314),
		_Utils_Tuple3(0.21708, 0.14087, 0.39964),
		_Utils_Tuple3(0.22111, 0.15223, 0.42558),
		_Utils_Tuple3(0.22500, 0.16354, 0.45096),
		_Utils_Tuple3(0.22875, 0.17481, 0.47578),
		_Utils_Tuple3(0.23236, 0.18603, 0.50004),
		_Utils_Tuple3(0.23582, 0.19720, 0.52373),
		_Utils_Tuple3(0.23915, 0.20833, 0.54686),
		_Utils_Tuple3(0.24234, 0.21941, 0.56942),
		_Utils_Tuple3(0.24539, 0.23044, 0.59142),
		_Utils_Tuple3(0.24830, 0.24143, 0.61286),
		_Utils_Tuple3(0.25107, 0.25237, 0.63374),
		_Utils_Tuple3(0.25369, 0.26327, 0.65406),
		_Utils_Tuple3(0.25618, 0.27412, 0.67381),
		_Utils_Tuple3(0.25853, 0.28492, 0.69300),
		_Utils_Tuple3(0.26074, 0.29568, 0.71162),
		_Utils_Tuple3(0.26280, 0.30639, 0.72968),
		_Utils_Tuple3(0.26473, 0.31706, 0.74718),
		_Utils_Tuple3(0.26652, 0.32768, 0.76412),
		_Utils_Tuple3(0.26816, 0.33825, 0.78050),
		_Utils_Tuple3(0.26967, 0.34878, 0.79631),
		_Utils_Tuple3(0.27103, 0.35926, 0.81156),
		_Utils_Tuple3(0.27226, 0.36970, 0.82624),
		_Utils_Tuple3(0.27334, 0.38008, 0.84037),
		_Utils_Tuple3(0.27429, 0.39043, 0.85393),
		_Utils_Tuple3(0.27509, 0.40072, 0.86692),
		_Utils_Tuple3(0.27576, 0.41097, 0.87936),
		_Utils_Tuple3(0.27628, 0.42118, 0.89123),
		_Utils_Tuple3(0.27667, 0.43134, 0.90254),
		_Utils_Tuple3(0.27691, 0.44145, 0.91328),
		_Utils_Tuple3(0.27701, 0.45152, 0.92347),
		_Utils_Tuple3(0.27698, 0.46153, 0.93309),
		_Utils_Tuple3(0.27680, 0.47151, 0.94214),
		_Utils_Tuple3(0.27648, 0.48144, 0.95064),
		_Utils_Tuple3(0.27603, 0.49132, 0.95857),
		_Utils_Tuple3(0.27543, 0.50115, 0.96594),
		_Utils_Tuple3(0.27469, 0.51094, 0.97275),
		_Utils_Tuple3(0.27381, 0.52069, 0.97899),
		_Utils_Tuple3(0.27273, 0.53040, 0.98461),
		_Utils_Tuple3(0.27106, 0.54015, 0.98930),
		_Utils_Tuple3(0.26878, 0.54995, 0.99303),
		_Utils_Tuple3(0.26592, 0.55979, 0.99583),
		_Utils_Tuple3(0.26252, 0.56967, 0.99773),
		_Utils_Tuple3(0.25862, 0.57958, 0.99876),
		_Utils_Tuple3(0.25425, 0.58950, 0.99896),
		_Utils_Tuple3(0.24946, 0.59943, 0.99835),
		_Utils_Tuple3(0.24427, 0.60937, 0.99697),
		_Utils_Tuple3(0.23874, 0.61931, 0.99485),
		_Utils_Tuple3(0.23288, 0.62923, 0.99202),
		_Utils_Tuple3(0.22676, 0.63913, 0.98851),
		_Utils_Tuple3(0.22039, 0.64901, 0.98436),
		_Utils_Tuple3(0.21382, 0.65886, 0.97959),
		_Utils_Tuple3(0.20708, 0.66866, 0.97423),
		_Utils_Tuple3(0.20021, 0.67842, 0.96833),
		_Utils_Tuple3(0.19326, 0.68812, 0.96190),
		_Utils_Tuple3(0.18625, 0.69775, 0.95498),
		_Utils_Tuple3(0.17923, 0.70732, 0.94761),
		_Utils_Tuple3(0.17223, 0.71680, 0.93981),
		_Utils_Tuple3(0.16529, 0.72620, 0.93161),
		_Utils_Tuple3(0.15844, 0.73551, 0.92305),
		_Utils_Tuple3(0.15173, 0.74472, 0.91416),
		_Utils_Tuple3(0.14519, 0.75381, 0.90496),
		_Utils_Tuple3(0.13886, 0.76279, 0.89550),
		_Utils_Tuple3(0.13278, 0.77165, 0.88580),
		_Utils_Tuple3(0.12698, 0.78037, 0.87590),
		_Utils_Tuple3(0.12151, 0.78896, 0.86581),
		_Utils_Tuple3(0.11639, 0.79740, 0.85559),
		_Utils_Tuple3(0.11167, 0.80569, 0.84525),
		_Utils_Tuple3(0.10738, 0.81381, 0.83484),
		_Utils_Tuple3(0.10357, 0.82177, 0.82437),
		_Utils_Tuple3(0.10026, 0.82955, 0.81389),
		_Utils_Tuple3(0.09750, 0.83714, 0.80342),
		_Utils_Tuple3(0.09532, 0.84455, 0.79299),
		_Utils_Tuple3(0.09377, 0.85175, 0.78264),
		_Utils_Tuple3(0.09287, 0.85875, 0.77240),
		_Utils_Tuple3(0.09267, 0.86554, 0.76230),
		_Utils_Tuple3(0.09320, 0.87211, 0.75237),
		_Utils_Tuple3(0.09451, 0.87844, 0.74265),
		_Utils_Tuple3(0.09662, 0.88454, 0.73316),
		_Utils_Tuple3(0.09958, 0.89040, 0.72393),
		_Utils_Tuple3(0.10342, 0.89600, 0.71500),
		_Utils_Tuple3(0.10815, 0.90142, 0.70599),
		_Utils_Tuple3(0.11374, 0.90673, 0.69651),
		_Utils_Tuple3(0.12014, 0.91193, 0.68660),
		_Utils_Tuple3(0.12733, 0.91701, 0.67627),
		_Utils_Tuple3(0.13526, 0.92197, 0.66556),
		_Utils_Tuple3(0.14391, 0.92680, 0.65448),
		_Utils_Tuple3(0.15323, 0.93151, 0.64308),
		_Utils_Tuple3(0.16319, 0.93609, 0.63137),
		_Utils_Tuple3(0.17377, 0.94053, 0.61938),
		_Utils_Tuple3(0.18491, 0.94484, 0.60713),
		_Utils_Tuple3(0.19659, 0.94901, 0.59466),
		_Utils_Tuple3(0.20877, 0.95304, 0.58199),
		_Utils_Tuple3(0.22142, 0.95692, 0.56914),
		_Utils_Tuple3(0.23449, 0.96065, 0.55614),
		_Utils_Tuple3(0.24797, 0.96423, 0.54303),
		_Utils_Tuple3(0.26180, 0.96765, 0.52981),
		_Utils_Tuple3(0.27597, 0.97092, 0.51653),
		_Utils_Tuple3(0.29042, 0.97403, 0.50321),
		_Utils_Tuple3(0.30513, 0.97697, 0.48987),
		_Utils_Tuple3(0.32006, 0.97974, 0.47654),
		_Utils_Tuple3(0.33517, 0.98234, 0.46325),
		_Utils_Tuple3(0.35043, 0.98477, 0.45002),
		_Utils_Tuple3(0.36581, 0.98702, 0.43688),
		_Utils_Tuple3(0.38127, 0.98909, 0.42386),
		_Utils_Tuple3(0.39678, 0.99098, 0.41098),
		_Utils_Tuple3(0.41229, 0.99268, 0.39826),
		_Utils_Tuple3(0.42778, 0.99419, 0.38575),
		_Utils_Tuple3(0.44321, 0.99551, 0.37345),
		_Utils_Tuple3(0.45854, 0.99663, 0.36140),
		_Utils_Tuple3(0.47375, 0.99755, 0.34963),
		_Utils_Tuple3(0.48879, 0.99828, 0.33816),
		_Utils_Tuple3(0.50362, 0.99879, 0.32701),
		_Utils_Tuple3(0.51822, 0.99910, 0.31622),
		_Utils_Tuple3(0.53255, 0.99919, 0.30581),
		_Utils_Tuple3(0.54658, 0.99907, 0.29581),
		_Utils_Tuple3(0.56026, 0.99873, 0.28623),
		_Utils_Tuple3(0.57357, 0.99817, 0.27712),
		_Utils_Tuple3(0.58646, 0.99739, 0.26849),
		_Utils_Tuple3(0.59891, 0.99638, 0.26038),
		_Utils_Tuple3(0.61088, 0.99514, 0.25280),
		_Utils_Tuple3(0.62233, 0.99366, 0.24579),
		_Utils_Tuple3(0.63323, 0.99195, 0.23937),
		_Utils_Tuple3(0.64362, 0.98999, 0.23356),
		_Utils_Tuple3(0.65394, 0.98775, 0.22835),
		_Utils_Tuple3(0.66428, 0.98524, 0.22370),
		_Utils_Tuple3(0.67462, 0.98246, 0.21960),
		_Utils_Tuple3(0.68494, 0.97941, 0.21602),
		_Utils_Tuple3(0.69525, 0.97610, 0.21294),
		_Utils_Tuple3(0.70553, 0.97255, 0.21032),
		_Utils_Tuple3(0.71577, 0.96875, 0.20815),
		_Utils_Tuple3(0.72596, 0.96470, 0.20640),
		_Utils_Tuple3(0.73610, 0.96043, 0.20504),
		_Utils_Tuple3(0.74617, 0.95593, 0.20406),
		_Utils_Tuple3(0.75617, 0.95121, 0.20343),
		_Utils_Tuple3(0.76608, 0.94627, 0.20311),
		_Utils_Tuple3(0.77591, 0.94113, 0.20310),
		_Utils_Tuple3(0.78563, 0.93579, 0.20336),
		_Utils_Tuple3(0.79524, 0.93025, 0.20386),
		_Utils_Tuple3(0.80473, 0.92452, 0.20459),
		_Utils_Tuple3(0.81410, 0.91861, 0.20552),
		_Utils_Tuple3(0.82333, 0.91253, 0.20663),
		_Utils_Tuple3(0.83241, 0.90627, 0.20788),
		_Utils_Tuple3(0.84133, 0.89986, 0.20926),
		_Utils_Tuple3(0.85010, 0.89328, 0.21074),
		_Utils_Tuple3(0.85868, 0.88655, 0.21230),
		_Utils_Tuple3(0.86709, 0.87968, 0.21391),
		_Utils_Tuple3(0.87530, 0.87267, 0.21555),
		_Utils_Tuple3(0.88331, 0.86553, 0.21719),
		_Utils_Tuple3(0.89112, 0.85826, 0.21880),
		_Utils_Tuple3(0.89870, 0.85087, 0.22038),
		_Utils_Tuple3(0.90605, 0.84337, 0.22188),
		_Utils_Tuple3(0.91317, 0.83576, 0.22328),
		_Utils_Tuple3(0.92004, 0.82806, 0.22456),
		_Utils_Tuple3(0.92666, 0.82025, 0.22570),
		_Utils_Tuple3(0.93301, 0.81236, 0.22667),
		_Utils_Tuple3(0.93909, 0.80439, 0.22744),
		_Utils_Tuple3(0.94489, 0.79634, 0.22800),
		_Utils_Tuple3(0.95039, 0.78823, 0.22831),
		_Utils_Tuple3(0.95560, 0.78005, 0.22836),
		_Utils_Tuple3(0.96049, 0.77181, 0.22811),
		_Utils_Tuple3(0.96507, 0.76352, 0.22754),
		_Utils_Tuple3(0.96931, 0.75519, 0.22663),
		_Utils_Tuple3(0.97323, 0.74682, 0.22536),
		_Utils_Tuple3(0.97679, 0.73842, 0.22369),
		_Utils_Tuple3(0.98000, 0.73000, 0.22161),
		_Utils_Tuple3(0.98289, 0.72140, 0.21918),
		_Utils_Tuple3(0.98549, 0.71250, 0.21650),
		_Utils_Tuple3(0.98781, 0.70330, 0.21358),
		_Utils_Tuple3(0.98986, 0.69382, 0.21043),
		_Utils_Tuple3(0.99163, 0.68408, 0.20706),
		_Utils_Tuple3(0.99314, 0.67408, 0.20348),
		_Utils_Tuple3(0.99438, 0.66386, 0.19971),
		_Utils_Tuple3(0.99535, 0.65341, 0.19577),
		_Utils_Tuple3(0.99607, 0.64277, 0.19165),
		_Utils_Tuple3(0.99654, 0.63193, 0.18738),
		_Utils_Tuple3(0.99675, 0.62093, 0.18297),
		_Utils_Tuple3(0.99672, 0.60977, 0.17842),
		_Utils_Tuple3(0.99644, 0.59846, 0.17376),
		_Utils_Tuple3(0.99593, 0.58703, 0.16899),
		_Utils_Tuple3(0.99517, 0.57549, 0.16412),
		_Utils_Tuple3(0.99419, 0.56386, 0.15918),
		_Utils_Tuple3(0.99297, 0.55214, 0.15417),
		_Utils_Tuple3(0.99153, 0.54036, 0.14910),
		_Utils_Tuple3(0.98987, 0.52854, 0.14398),
		_Utils_Tuple3(0.98799, 0.51667, 0.13883),
		_Utils_Tuple3(0.98590, 0.50479, 0.13367),
		_Utils_Tuple3(0.98360, 0.49291, 0.12849),
		_Utils_Tuple3(0.98108, 0.48104, 0.12332),
		_Utils_Tuple3(0.97837, 0.46920, 0.11817),
		_Utils_Tuple3(0.97545, 0.45740, 0.11305),
		_Utils_Tuple3(0.97234, 0.44565, 0.10797),
		_Utils_Tuple3(0.96904, 0.43399, 0.10294),
		_Utils_Tuple3(0.96555, 0.42241, 0.09798),
		_Utils_Tuple3(0.96187, 0.41093, 0.09310),
		_Utils_Tuple3(0.95801, 0.39958, 0.08831),
		_Utils_Tuple3(0.95398, 0.38836, 0.08362),
		_Utils_Tuple3(0.94977, 0.37729, 0.07905),
		_Utils_Tuple3(0.94538, 0.36638, 0.07461),
		_Utils_Tuple3(0.94084, 0.35566, 0.07031),
		_Utils_Tuple3(0.93612, 0.34513, 0.06616),
		_Utils_Tuple3(0.93125, 0.33482, 0.06218),
		_Utils_Tuple3(0.92623, 0.32473, 0.05837),
		_Utils_Tuple3(0.92105, 0.31489, 0.05475),
		_Utils_Tuple3(0.91572, 0.30530, 0.05134),
		_Utils_Tuple3(0.91024, 0.29599, 0.04814),
		_Utils_Tuple3(0.90463, 0.28696, 0.04516),
		_Utils_Tuple3(0.89888, 0.27824, 0.04243),
		_Utils_Tuple3(0.89298, 0.26981, 0.03993),
		_Utils_Tuple3(0.88691, 0.26152, 0.03753),
		_Utils_Tuple3(0.88066, 0.25334, 0.03521),
		_Utils_Tuple3(0.87422, 0.24526, 0.03297),
		_Utils_Tuple3(0.86760, 0.23730, 0.03082),
		_Utils_Tuple3(0.86079, 0.22945, 0.02875),
		_Utils_Tuple3(0.85380, 0.22170, 0.02677),
		_Utils_Tuple3(0.84662, 0.21407, 0.02487),
		_Utils_Tuple3(0.83926, 0.20654, 0.02305),
		_Utils_Tuple3(0.83172, 0.19912, 0.02131),
		_Utils_Tuple3(0.82399, 0.19182, 0.01966),
		_Utils_Tuple3(0.81608, 0.18462, 0.01809),
		_Utils_Tuple3(0.80799, 0.17753, 0.01660),
		_Utils_Tuple3(0.79971, 0.17055, 0.01520),
		_Utils_Tuple3(0.79125, 0.16368, 0.01387),
		_Utils_Tuple3(0.78260, 0.15693, 0.01264),
		_Utils_Tuple3(0.77377, 0.15028, 0.01148),
		_Utils_Tuple3(0.76476, 0.14374, 0.01041),
		_Utils_Tuple3(0.75556, 0.13731, 0.00942),
		_Utils_Tuple3(0.74617, 0.13098, 0.00851),
		_Utils_Tuple3(0.73661, 0.12477, 0.00769),
		_Utils_Tuple3(0.72686, 0.11867, 0.00695),
		_Utils_Tuple3(0.71692, 0.11268, 0.00629),
		_Utils_Tuple3(0.70680, 0.10680, 0.00571),
		_Utils_Tuple3(0.69650, 0.10102, 0.00522),
		_Utils_Tuple3(0.68602, 0.09536, 0.00481),
		_Utils_Tuple3(0.67535, 0.08980, 0.00449),
		_Utils_Tuple3(0.66449, 0.08436, 0.00424),
		_Utils_Tuple3(0.65345, 0.07902, 0.00408),
		_Utils_Tuple3(0.64223, 0.07380, 0.00401),
		_Utils_Tuple3(0.63082, 0.06868, 0.00401),
		_Utils_Tuple3(0.61923, 0.06367, 0.00410),
		_Utils_Tuple3(0.60746, 0.05878, 0.00427),
		_Utils_Tuple3(0.59550, 0.05399, 0.00453),
		_Utils_Tuple3(0.58336, 0.04931, 0.00486),
		_Utils_Tuple3(0.57103, 0.04474, 0.00529),
		_Utils_Tuple3(0.55852, 0.04028, 0.00579),
		_Utils_Tuple3(0.54583, 0.03593, 0.00638),
		_Utils_Tuple3(0.53295, 0.03169, 0.00705),
		_Utils_Tuple3(0.51989, 0.02756, 0.00780),
		_Utils_Tuple3(0.50664, 0.02354, 0.00863),
		_Utils_Tuple3(0.49321, 0.01963, 0.00955),
		_Utils_Tuple3(0.47960, 0.01583, 0.01055)
	]);
var $author$project$Canvas$getColor = F2(
	function (_v0, targetValue) {
		var valueMin = _v0.a;
		var valueMax = _v0.b;
		var value = A2(
			$elm$core$Basics$min,
			valueMax,
			A2($elm$core$Basics$max, targetValue, valueMin));
		var interval = (valueMax - valueMin) / 256.0;
		var range = A2(
			$elm$core$List$take,
			2,
			A2(
				$elm$core$List$filter,
				function (_v8) {
					var upper = _v8.b;
					return _Utils_cmp(value, upper) < 1;
				},
				A2(
					$elm$core$List$indexedMap,
					F2(
						function (i, rgb) {
							return _Utils_Tuple3(valueMin + (i * interval), valueMin + ((i + 1) * interval), rgb);
						}),
					$author$project$Canvas$turboColormapData)));
		if (range.b) {
			if (range.b.b) {
				var _v2 = range.a;
				var lower1 = _v2.a;
				var _v3 = _v2.c;
				var r1 = _v3.a;
				var g1 = _v3.b;
				var b1 = _v3.c;
				var _v4 = range.b;
				var _v5 = _v4.a;
				var _v6 = _v5.c;
				var r2 = _v6.a;
				var g2 = _v6.b;
				var b2 = _v6.c;
				return _Utils_Tuple3(r1 + (((r2 - r1) * (value - lower1)) / interval), g1 + (((g2 - g1) * (value - lower1)) / interval), b1 + (((b2 - b1) * (value - lower1)) / interval));
			} else {
				var _v7 = range.a;
				var rgb = _v7.c;
				return rgb;
			}
		} else {
			return _Utils_Tuple3(0.0, 0.0, 0.0);
		}
	});
var $elm$svg$Svg$line = $elm$svg$Svg$trustedNode('line');
var $avh4$elm_color$Color$RgbaSpace = F4(
	function (a, b, c, d) {
		return {$: 'RgbaSpace', a: a, b: b, c: c, d: d};
	});
var $avh4$elm_color$Color$rgb = F3(
	function (r, g, b) {
		return A4($avh4$elm_color$Color$RgbaSpace, r, g, b, 1.0);
	});
var $elm$core$String$concat = function (strings) {
	return A2($elm$core$String$join, '', strings);
};
var $elm$core$Basics$round = _Basics_round;
var $avh4$elm_color$Color$toCssString = function (_v0) {
	var r = _v0.a;
	var g = _v0.b;
	var b = _v0.c;
	var a = _v0.d;
	var roundTo = function (x) {
		return $elm$core$Basics$round(x * 1000) / 1000;
	};
	var pct = function (x) {
		return $elm$core$Basics$round(x * 10000) / 100;
	};
	return $elm$core$String$concat(
		_List_fromArray(
			[
				'rgba(',
				$elm$core$String$fromFloat(
				pct(r)),
				'%,',
				$elm$core$String$fromFloat(
				pct(g)),
				'%,',
				$elm$core$String$fromFloat(
				pct(b)),
				'%,',
				$elm$core$String$fromFloat(
				roundTo(a)),
				')'
			]));
};
var $elm$svg$Svg$Attributes$x1 = _VirtualDom_attribute('x1');
var $elm$svg$Svg$Attributes$x2 = _VirtualDom_attribute('x2');
var $elm$svg$Svg$Attributes$y1 = _VirtualDom_attribute('y1');
var $elm$svg$Svg$Attributes$y2 = _VirtualDom_attribute('y2');
var $author$project$Canvas$drawContourLine = F2(
	function (_v0, cline) {
		var valueMin = _v0.a;
		var valueMax = _v0.b;
		var line = cline.line;
		var _v1 = A2(
			$author$project$Canvas$getColor,
			_Utils_Tuple2(valueMin, valueMax),
			cline.value);
		var r = _v1.a;
		var g = _v1.b;
		var b = _v1.c;
		return _List_fromArray(
			[
				A2(
				$elm$svg$Svg$line,
				_List_fromArray(
					[
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x1, line.x1),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y1, line.y1),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x2, line.x2),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y2, line.y2),
						$elm$svg$Svg$Attributes$stroke(
						$avh4$elm_color$Color$toCssString(
							A3($avh4$elm_color$Color$rgb, r, g, b))),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$strokeWidth, line.strokeWidth)
					]),
				_List_Nil)
			]);
	});
var $elm$svg$Svg$Attributes$points = _VirtualDom_attribute('points');
var $elm$svg$Svg$polygon = $elm$svg$Svg$trustedNode('polygon');
var $author$project$Canvas$drawContourPolygon = F2(
	function (_v0, cpolygon) {
		var valueMin = _v0.a;
		var valueMax = _v0.b;
		var polygon = cpolygon.polygon;
		var _v1 = A2(
			$author$project$Canvas$getColor,
			_Utils_Tuple2(valueMin, valueMax),
			cpolygon.value);
		var r = _v1.a;
		var g = _v1.b;
		var b = _v1.c;
		return _List_fromArray(
			[
				A2(
				$elm$svg$Svg$polygon,
				_List_fromArray(
					[
						$elm$svg$Svg$Attributes$points(
						A2(
							$elm$core$String$join,
							' ',
							A2(
								$elm$core$List$map,
								function (p) {
									return A2(
										$elm$core$String$join,
										',',
										A2(
											$elm$core$List$map,
											function (v) {
												return $elm$core$String$fromFloat(v);
											},
											_List_fromArray(
												[p.x, p.y])));
								},
								polygon.points))),
						$elm$svg$Svg$Attributes$stroke(
						$avh4$elm_color$Color$toCssString(
							A3($avh4$elm_color$Color$rgb, r, g, b))),
						$elm$svg$Svg$Attributes$fill(
						$avh4$elm_color$Color$toCssString(
							A3($avh4$elm_color$Color$rgb, r, g, b))),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$opacity, polygon.style.opacity),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$strokeWidth, polygon.style.strokeWidth)
					]),
				_List_Nil)
			]);
	});
var $author$project$Canvas$drawLine = function (line) {
	return _List_fromArray(
		[
			A2(
			$elm$svg$Svg$line,
			_List_fromArray(
				[
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x1, line.x1),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y1, line.y1),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x2, line.x2),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y2, line.y2),
					$elm$svg$Svg$Attributes$stroke(line.stroke),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$strokeWidth, line.strokeWidth)
				]),
			_List_Nil)
		]);
};
var $elm$virtual_dom$VirtualDom$text = _VirtualDom_text;
var $elm$html$Html$text = $elm$virtual_dom$VirtualDom$text;
var $elm$svg$Svg$Attributes$textAnchor = _VirtualDom_attribute('text-anchor');
var $elm$svg$Svg$text_ = $elm$svg$Svg$trustedNode('text');
var $elm$svg$Svg$Attributes$transform = _VirtualDom_attribute('transform');
var $author$project$Canvas$drawLineText = F2(
	function (config, lineText) {
		var text = lineText.text;
		var fontHeight = config.fontSize;
		var offsetHeight = (lineText.dominantBaseLine === 'text-after-edge') ? (((-1.0) * $elm$core$Basics$abs(lineText.offsetFontHeight)) * fontHeight) : ((lineText.dominantBaseLine === 'text-before-edge') ? ($elm$core$Basics$abs(lineText.offsetFontHeight) * fontHeight) : (lineText.offsetFontHeight * fontHeight));
		var _v0 = lineText;
		var x1 = _v0.x1;
		var y1 = _v0.y1;
		var x2 = _v0.x2;
		var y2 = _v0.y2;
		var x = x1 + ((x2 - x1) * lineText.ratio);
		var y = y1 + ((y2 - y1) * lineText.ratio);
		var transformRotate = 'rotate(' + (A2(
			$elm$core$String$join,
			',',
			A2(
				$elm$core$List$map,
				$elm$core$String$fromFloat,
				_List_fromArray(
					[(-1.0) * lineText.rotate, x, y]))) + ')');
		return _List_fromArray(
			[
				A2(
				$elm$svg$Svg$text_,
				_List_fromArray(
					[
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x, x),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y, y + offsetHeight),
						$elm$svg$Svg$Attributes$transform(transformRotate),
						$elm$svg$Svg$Attributes$fill(lineText.fill),
						$elm$svg$Svg$Attributes$stroke(lineText.stroke),
						$elm$svg$Svg$Attributes$textAnchor(lineText.textAnchor),
						$elm$svg$Svg$Attributes$dominantBaseline(lineText.dominantBaseLine)
					]),
				_List_fromArray(
					[
						$elm$html$Html$text(text)
					]))
			]);
	});
var $elm$svg$Svg$Attributes$d = _VirtualDom_attribute('d');
var $elm$core$Basics$cos = _Basics_cos;
var $elm$core$Basics$pi = _Basics_pi;
var $elm$core$Basics$degrees = function (angleInDegrees) {
	return (angleInDegrees * $elm$core$Basics$pi) / 180;
};
var $elm$core$Basics$sin = _Basics_sin;
var $elm$core$Basics$pow = _Basics_pow;
var $author$project$Canvas$unitLineVector = function (line) {
	var dy = A2($elm$core$Debug$log, 'dy', line.y2 - line.y1);
	var dx = A2($elm$core$Debug$log, 'dx', line.x2 - line.x1);
	var factor = A2(
		$elm$core$Debug$log,
		'factor',
		1.0 / A2(
			$elm$core$Basics$pow,
			A2($elm$core$Basics$pow, dx, 2.0) + A2($elm$core$Basics$pow, dy, 2.0),
			0.5));
	return A2(
		$elm_explorations$linear_algebra$Math$Vector2$scale,
		factor,
		A2($elm_explorations$linear_algebra$Math$Vector2$vec2, dx, dy));
};
var $author$project$Canvas$diagonalVector = function (line) {
	var unitLineVec = $author$project$Canvas$unitLineVector(line);
	var dy = $elm_explorations$linear_algebra$Math$Vector2$getY(unitLineVec);
	var dx = $elm_explorations$linear_algebra$Math$Vector2$getX(unitLineVec);
	var vecx = (dx * $elm$core$Basics$cos(
		$elm$core$Basics$degrees(90.0))) - (dy * $elm$core$Basics$sin(
		$elm$core$Basics$degrees(90.0)));
	var vecy = (dx * $elm$core$Basics$sin(
		$elm$core$Basics$degrees(90.0))) + (dy * $elm$core$Basics$cos(
		$elm$core$Basics$degrees(90.0)));
	return A2($elm_explorations$linear_algebra$Math$Vector2$vec2, vecx, vecy);
};
var $elm_explorations$linear_algebra$Math$Vector2$negate = _MJS_v2negate;
var $author$project$Canvas$momentCurveControlPoints = F2(
	function (scalableFactor, mline) {
		var scale2 = mline.m2 * scalableFactor;
		var scale1 = mline.m1 * scalableFactor;
		var m0 = mline.m0;
		var mc = m0 - (0.5 * (mline.m2 - mline.m1));
		var line = mline.line;
		var diagUnitVec1 = $author$project$Canvas$diagonalVector(line);
		var diagUnitVec2 = $elm_explorations$linear_algebra$Math$Vector2$negate(diagUnitVec1);
		var offset2x = $elm_explorations$linear_algebra$Math$Vector2$getX(diagUnitVec2) * scale2;
		var offset2y = $elm_explorations$linear_algebra$Math$Vector2$getY(diagUnitVec2) * scale2;
		var offset1x = $elm_explorations$linear_algebra$Math$Vector2$getX(diagUnitVec1) * scale1;
		var offset1y = $elm_explorations$linear_algebra$Math$Vector2$getY(diagUnitVec1) * scale1;
		var _v0 = _Utils_Tuple2(line.x2, line.y2);
		var x2 = _v0.a;
		var y2 = _v0.b;
		var _v1 = _Utils_Tuple2(x2 + offset2x, y2 + offset2y);
		var xr = _v1.a;
		var yr = _v1.b;
		var _v2 = _Utils_Tuple2(line.x1, line.y1);
		var x1 = _v2.a;
		var y1 = _v2.b;
		var _v3 = _Utils_Tuple2(x1 + offset1x, y1 + offset1y);
		var xl = _v3.a;
		var yl = _v3.b;
		var _v4 = _Utils_Tuple2(
			$elm_explorations$linear_algebra$Math$Vector2$getX(diagUnitVec1),
			$elm_explorations$linear_algebra$Math$Vector2$getY(diagUnitVec1));
		var ix = _v4.a;
		var iy = _v4.b;
		var _v5 = _Utils_Tuple2((0.5 * (x1 + x2)) + ((scalableFactor * mc) * ix), (0.5 * (y1 + y2)) + ((scalableFactor * mc) * iy));
		var xc = _v5.a;
		var yc = _v5.b;
		var cx1 = (((4.0 / 3.0) * xc) + ((1.0 / 12.0) * xl)) - ((5.0 / 12.0) * xr);
		var cx2 = (((4.0 / 3.0) * xc) - ((5.0 / 12.0) * xl)) + ((1.0 / 12.0) * xr);
		var cy1 = (((4.0 / 3.0) * yc) + ((1.0 / 12.0) * yl)) - ((5.0 / 12.0) * yr);
		var cy2 = (((4.0 / 3.0) * yc) - ((5.0 / 12.0) * yl)) + ((1.0 / 12.0) * yr);
		return (mline.m0 === 0.0) ? $elm$core$Maybe$Nothing : $elm$core$Maybe$Just(
			_Utils_Tuple2(
				_Utils_Tuple2(cx1, cy1),
				_Utils_Tuple2(cx2, cy2)));
	});
var $elm$svg$Svg$path = $elm$svg$Svg$trustedNode('path');
var $author$project$Canvas$drawMomentLine = F2(
	function (scalableFactor, mline) {
		var scale2 = mline.m2 * scalableFactor;
		var scale1 = mline.m1 * scalableFactor;
		var line = mline.line;
		var x1 = line.x1;
		var x2 = line.x2;
		var y1 = line.y1;
		var y2 = line.y2;
		var dy = line.y2 - line.y1;
		var dx = line.x2 - line.x1;
		var diagUnitVec1 = $author$project$Canvas$diagonalVector(line);
		var diagUnitVec2 = $elm_explorations$linear_algebra$Math$Vector2$negate(diagUnitVec1);
		var offset2x = $elm_explorations$linear_algebra$Math$Vector2$getX(diagUnitVec2) * scale2;
		var offset2y = $elm_explorations$linear_algebra$Math$Vector2$getY(diagUnitVec2) * scale2;
		var offset1x = $elm_explorations$linear_algebra$Math$Vector2$getX(diagUnitVec1) * scale1;
		var offset1y = $elm_explorations$linear_algebra$Math$Vector2$getY(diagUnitVec1) * scale1;
		var d = function () {
			var _v0 = A2($author$project$Canvas$momentCurveControlPoints, scalableFactor, mline);
			if (_v0.$ === 'Nothing') {
				return ' M ' + ($elm$core$String$fromFloat(line.x2) + (' ' + ($elm$core$String$fromFloat(line.y2) + (' l ' + ($elm$core$String$fromFloat(-dx) + (' ' + ($elm$core$String$fromFloat(-dy) + (' l ' + ($elm$core$String$fromFloat(offset1x) + (' ' + ($elm$core$String$fromFloat(offset1y) + (' l ' + ($elm$core$String$fromFloat(((offset1x * (-1.0)) + dx) + offset2x) + (' ' + ($elm$core$String$fromFloat(((offset1y * (-1.0)) + dy) + offset2y) + ' z')))))))))))))));
			} else {
				var controlPoints = _v0.a;
				var dcy2 = (y2 + offset2y) - (y1 + offset1y);
				var dcx2 = (x2 + offset2x) - (x1 + offset1x);
				var _v1 = controlPoints;
				var _v2 = _v1.a;
				var cx1 = _v2.a;
				var cy1 = _v2.b;
				var _v3 = _v1.b;
				var cx2 = _v3.a;
				var cy2 = _v3.b;
				var dcx0 = cx1 - (x1 + offset1x);
				var dcx1 = cx2 - (x1 + offset1x);
				var dcy0 = cy1 - (y1 + offset1y);
				var dcy1 = cy2 - (y1 + offset1y);
				var cString = A2(
					$elm$core$String$join,
					' ',
					A2(
						$elm$core$List$map,
						$elm$core$String$fromFloat,
						_List_fromArray(
							[dcx0, dcy0, dcx1, dcy1, dcx2, dcy2])));
				return ' M ' + ($elm$core$String$fromFloat(line.x2) + (' ' + ($elm$core$String$fromFloat(line.y2) + (' l ' + ($elm$core$String$fromFloat(-dx) + (' ' + ($elm$core$String$fromFloat(-dy) + (' l ' + ($elm$core$String$fromFloat(offset1x) + (' ' + ($elm$core$String$fromFloat(offset1y) + (' c ' + (cString + ' z')))))))))))));
			}
		}();
		return _List_fromArray(
			[
				A2(
				$elm$svg$Svg$path,
				_List_fromArray(
					[
						$elm$svg$Svg$Attributes$d(d),
						$elm$svg$Svg$Attributes$stroke('blue'),
						$elm$svg$Svg$Attributes$strokeWidth('1.0'),
						$elm$svg$Svg$Attributes$fill('lightblue'),
						$elm$svg$Svg$Attributes$opacity('0.5')
					]),
				_List_Nil)
			]);
	});
var $author$project$Canvas$drawPolygon = function (polygon) {
	return _List_fromArray(
		[
			A2(
			$elm$svg$Svg$polygon,
			_List_fromArray(
				[
					$elm$svg$Svg$Attributes$points(
					A2(
						$elm$core$String$join,
						' ',
						A2(
							$elm$core$List$map,
							function (p) {
								return A2(
									$elm$core$String$join,
									',',
									A2(
										$elm$core$List$map,
										function (v) {
											return $elm$core$String$fromFloat(v);
										},
										_List_fromArray(
											[p.x, p.y])));
							},
							polygon.points))),
					$elm$svg$Svg$Attributes$stroke(polygon.style.stroke),
					$elm$svg$Svg$Attributes$fill(polygon.style.fill),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$opacity, polygon.style.opacity),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$strokeWidth, polygon.style.strokeWidth)
				]),
			_List_Nil)
		]);
};
var $author$project$Canvas$drawRectangle = function (rect) {
	return _List_fromArray(
		[
			A2(
			$elm$svg$Svg$rect,
			_List_fromArray(
				[
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x, rect.x),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y, rect.y),
					$elm$svg$Svg$Attributes$stroke(rect.style.stroke),
					$elm$svg$Svg$Attributes$fill(rect.style.fill),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$opacity, rect.style.opacity),
					A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$strokeWidth, rect.style.strokeWidth)
				]),
			_List_Nil)
		]);
};
var $author$project$Canvas$drawScalableCircle = F2(
	function (scalableFactor, scircle) {
		var radius = scircle.value * scalableFactor;
		var circle = scircle.circle;
		return _List_fromArray(
			[
				A2(
				$elm$svg$Svg$circle,
				_List_fromArray(
					[
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$cx, circle.cx),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$cy, circle.cy),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$r, radius),
						$elm$svg$Svg$Attributes$stroke(circle.style.stroke),
						$elm$svg$Svg$Attributes$fill(circle.style.fill),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$opacity, circle.style.opacity),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$strokeWidth, circle.style.strokeWidth)
					]),
				_List_Nil)
			]);
	});
var $author$project$Canvas$drawScalableLine = F2(
	function (factor, sline) {
		var line = sline.line;
		return _List_fromArray(
			[
				A2(
				$elm$svg$Svg$line,
				_List_fromArray(
					[
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x1, line.x1 + (sline.dx1 * factor)),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y1, line.y1 + (sline.dy1 * factor)),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x2, line.x2 + (sline.dx2 * factor)),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y2, line.y2 + (sline.dy2 * factor)),
						$elm$svg$Svg$Attributes$stroke(line.stroke),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$strokeWidth, line.strokeWidth)
					]),
				_List_Nil)
			]);
	});
var $author$project$Canvas$drawText = F2(
	function (config, t) {
		var transformRotate = 'rotate(' + (A2(
			$elm$core$String$join,
			',',
			A2(
				$elm$core$List$map,
				$elm$core$String$fromFloat,
				_List_fromArray(
					[(-1.0) * t.rotate, t.x, t.y]))) + ')');
		var fontHeight = config.fontSize;
		var offsetHeight = (t.dominantBaseLine === 'text-after-edge') ? (((-1.0) * $elm$core$Basics$abs(t.offsetFontHeight)) * fontHeight) : ((t.dominantBaseLine === 'text-before-edge') ? ($elm$core$Basics$abs(t.offsetFontHeight) * fontHeight) : (t.offsetFontHeight * fontHeight));
		return _List_fromArray(
			[
				A2(
				$elm$svg$Svg$text_,
				_List_fromArray(
					[
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x, t.x),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y, t.y + offsetHeight),
						$elm$svg$Svg$Attributes$transform(transformRotate),
						$elm$svg$Svg$Attributes$fill(t.fill),
						$elm$svg$Svg$Attributes$stroke(t.stroke),
						$elm$svg$Svg$Attributes$textAnchor(t.textAnchor),
						$elm$svg$Svg$Attributes$dominantBaseline(t.dominantBaseLine)
					]),
				_List_fromArray(
					[
						$elm$html$Html$text(t.text)
					]))
			]);
	});
var $elm$core$List$any = F2(
	function (isOkay, list) {
		any:
		while (true) {
			if (!list.b) {
				return false;
			} else {
				var x = list.a;
				var xs = list.b;
				if (isOkay(x)) {
					return true;
				} else {
					var $temp$isOkay = isOkay,
						$temp$list = xs;
					isOkay = $temp$isOkay;
					list = $temp$list;
					continue any;
				}
			}
		}
	});
var $elm$core$Basics$not = _Basics_not;
var $elm$core$List$all = F2(
	function (isOkay, list) {
		return !A2(
			$elm$core$List$any,
			A2($elm$core$Basics$composeL, $elm$core$Basics$not, isOkay),
			list);
	});
var $author$project$Canvas$filterEntities = F2(
	function (tags, entities) {
		var deactiveTagDict = $elm$core$Dict$fromList(
			A2(
				$elm$core$List$map,
				function (tag) {
					return _Utils_Tuple2(tag.key, tag);
				},
				A2(
					$elm$core$List$filter,
					function (tag) {
						return !tag.activated;
					},
					tags)));
		return A2(
			$elm$core$List$filter,
			function (entity) {
				return A2(
					$elm$core$List$all,
					function (tagKey) {
						var _v0 = A2($elm$core$Dict$get, tagKey, deactiveTagDict);
						if (_v0.$ === 'Nothing') {
							return true;
						} else {
							return false;
						}
					},
					entity.tags);
			},
			entities);
	});
var $author$project$Canvas$drawLayer = F3(
	function (config, tags, layer) {
		var filter = $author$project$Canvas$filterEntities(tags);
		var lineTexts = filter(layer.lineTexts);
		var lines = filter(layer.lines);
		var momentLines = A2(
			$elm$core$List$map,
			function (withTags) {
				return withTags.entity;
			},
			filter(
				A2(
					$elm$core$List$map,
					function (entity) {
						return {entity: entity, tags: entity.line.tags};
					},
					layer.momentLines)));
		var polygons = filter(layer.polygons);
		var rectangles = filter(layer.rectangles);
		var scalableCircles = A2(
			$elm$core$List$map,
			function (withTags) {
				return withTags.entity;
			},
			filter(
				A2(
					$elm$core$List$map,
					function (entity) {
						return {entity: entity, tags: entity.circle.tags};
					},
					layer.scalableCircles)));
		var scalableLines = A2(
			$elm$core$List$map,
			function (withTags) {
				return withTags.entity;
			},
			filter(
				A2(
					$elm$core$List$map,
					function (entity) {
						return {entity: entity, tags: entity.line.tags};
					},
					layer.scalableLines)));
		var texts = filter(layer.texts);
		var contourPolygons = A2(
			$elm$core$List$map,
			function (withTags) {
				return withTags.entity;
			},
			filter(
				A2(
					$elm$core$List$map,
					function (entity) {
						return {entity: entity, tags: entity.polygon.tags};
					},
					layer.contourPolygons)));
		var contourLines = A2(
			$elm$core$List$map,
			function (withTags) {
				return withTags.entity;
			},
			filter(
				A2(
					$elm$core$List$map,
					function (entity) {
						return {entity: entity, tags: entity.line.tags};
					},
					layer.contourLines)));
		var circles = filter(layer.circles);
		return $elm$core$List$concat(
			_List_fromArray(
				[
					A2($elm$core$List$concatMap, $author$project$Canvas$drawLine, lines),
					A2($elm$core$List$concatMap, $author$project$Canvas$drawCircle, circles),
					A2($elm$core$List$concatMap, $author$project$Canvas$drawRectangle, rectangles),
					A2($elm$core$List$concatMap, $author$project$Canvas$drawPolygon, polygons),
					A2(
					$elm$core$List$concatMap,
					function (entity) {
						return A2($author$project$Canvas$drawScalableLine, config.scalableFactors.scalableLine, entity);
					},
					scalableLines),
					A2(
					$elm$core$List$concatMap,
					function (entity) {
						return A2($author$project$Canvas$drawScalableCircle, config.scalableFactors.scalableCircle, entity);
					},
					scalableCircles),
					A2(
					$elm$core$List$concatMap,
					function (entity) {
						return A2(
							$author$project$Canvas$drawContourLine,
							_Utils_Tuple2(config.contourMin, config.contourMax),
							entity);
					},
					contourLines),
					A2(
					$elm$core$List$concatMap,
					function (entity) {
						return A2(
							$author$project$Canvas$drawContourPolygon,
							_Utils_Tuple2(config.contourMin, config.contourMax),
							entity);
					},
					contourPolygons),
					A2(
					$elm$core$List$concatMap,
					function (entity) {
						return A2($author$project$Canvas$drawMomentLine, config.scalableFactors.momentLine, entity);
					},
					momentLines),
					A2(
					$elm$core$List$concatMap,
					$author$project$Canvas$drawText(config),
					texts),
					A2(
					$elm$core$List$concatMap,
					$author$project$Canvas$drawLineText(config),
					lineTexts)
				]));
	});
var $author$project$Canvas$drawModel = function (model) {
	var entities = model.entities;
	var xaxisPositions = A2(
		$elm$core$List$map,
		function (axis) {
			return axis.position;
		},
		entities.xaxes);
	var xaxisEnd = function () {
		var _v3 = $elm$core$List$maximum(xaxisPositions);
		if (_v3.$ === 'Just') {
			var v = _v3.a;
			return v;
		} else {
			return 0.0;
		}
	}();
	var xaxisStart = function () {
		var _v2 = $elm$core$List$minimum(xaxisPositions);
		if (_v2.$ === 'Just') {
			var v = _v2.a;
			return v;
		} else {
			return 0.0;
		}
	}();
	var yaxisPositions = A2(
		$elm$core$List$map,
		function (axis) {
			return axis.position;
		},
		entities.yaxes);
	var yaxisEnd = function () {
		var _v1 = $elm$core$List$maximum(yaxisPositions);
		if (_v1.$ === 'Just') {
			var v = _v1.a;
			return v;
		} else {
			return 0.0;
		}
	}();
	var yaxisStart = function () {
		var _v0 = $elm$core$List$minimum(yaxisPositions);
		if (_v0.$ === 'Just') {
			var v = _v0.a;
			return v;
		} else {
			return 0.0;
		}
	}();
	var drawingObjects = $elm$core$List$concat(
		A2(
			$elm$core$List$map,
			A2($author$project$Canvas$drawLayer, model.config, model.tags),
			model.entities.layers));
	var config = model.config;
	var xaxisY = config.height - (0.5 * config.margin);
	var xaxes = A2(
		$elm$core$List$append,
		_List_fromArray(
			[
				A2(
				$elm$svg$Svg$line,
				_List_fromArray(
					[
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x1, xaxisStart),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x2, xaxisEnd),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y1, xaxisY),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y2, xaxisY)
					]),
				_List_Nil)
			]),
		$elm$core$List$concat(
			A2(
				$elm$core$List$map,
				function (axis) {
					return _List_fromArray(
						[
							A2(
							$elm$svg$Svg$line,
							_List_fromArray(
								[
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x1, axis.position),
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x2, axis.position),
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y1, xaxisY),
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y2, xaxisY - 10),
									$elm$svg$Svg$Attributes$stroke('black'),
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$strokeWidth, 1)
								]),
							_List_Nil),
							A2(
							$elm$svg$Svg$text_,
							_List_fromArray(
								[
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x, axis.position),
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y, xaxisY),
									$elm$svg$Svg$Attributes$stroke('black'),
									$elm$svg$Svg$Attributes$fill('black'),
									$elm$svg$Svg$Attributes$textAnchor('middle'),
									$elm$svg$Svg$Attributes$dominantBaseline('text-before-edge')
								]),
							_List_fromArray(
								[
									$elm$html$Html$text(axis.name)
								]))
						]);
				},
				entities.xaxes)));
	var yaxisX = 0.5 * config.margin;
	var yaxes = A2(
		$elm$core$List$append,
		_List_fromArray(
			[
				A2(
				$elm$svg$Svg$line,
				_List_fromArray(
					[
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x1, yaxisX),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x2, yaxisX),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y1, yaxisStart),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y2, yaxisEnd)
					]),
				_List_Nil)
			]),
		$elm$core$List$concat(
			A2(
				$elm$core$List$map,
				function (axis) {
					return _List_fromArray(
						[
							A2(
							$elm$svg$Svg$line,
							_List_fromArray(
								[
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y1, axis.position),
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y2, axis.position),
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x1, yaxisX),
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x2, yaxisX + 10),
									$elm$svg$Svg$Attributes$stroke('black'),
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$strokeWidth, 1)
								]),
							_List_Nil),
							A2(
							$elm$svg$Svg$text_,
							_List_fromArray(
								[
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x, yaxisX - 5),
									A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y, axis.position),
									$elm$svg$Svg$Attributes$stroke('black'),
									$elm$svg$Svg$Attributes$fill('black'),
									$elm$svg$Svg$Attributes$textAnchor('end'),
									$elm$svg$Svg$Attributes$dominantBaseline('middle')
								]),
							_List_fromArray(
								[
									$elm$html$Html$text(axis.name)
								]))
						]);
				},
				entities.yaxes)));
	return $elm$core$List$concat(
		_List_fromArray(
			[drawingObjects, xaxes, yaxes]));
};
var $elm$svg$Svg$Attributes$fontSize = _VirtualDom_attribute('font-size');
var $elm$svg$Svg$g = $elm$svg$Svg$trustedNode('g');
var $elm$virtual_dom$VirtualDom$Custom = function (a) {
	return {$: 'Custom', a: a};
};
var $elm$virtual_dom$VirtualDom$on = _VirtualDom_on;
var $elm$html$Html$Events$custom = F2(
	function (event, decoder) {
		return A2(
			$elm$virtual_dom$VirtualDom$on,
			event,
			$elm$virtual_dom$VirtualDom$Custom(decoder));
	});
var $author$project$Canvas$handleZoom = function (onZoom) {
	var zoomDecoder = A2(
		$elm$json$Json$Decode$map,
		onZoom,
		A2($elm$json$Json$Decode$field, 'deltaY', $elm$json$Json$Decode$float));
	var alwaysPreventDefaultAndStopPropagation = function (msg) {
		return {message: msg, preventDefault: true, stopPropagation: true};
	};
	return A2(
		$elm$html$Html$Events$custom,
		'wheel',
		A2($elm$json$Json$Decode$map, alwaysPreventDefaultAndStopPropagation, zoomDecoder));
};
var $elm$html$Html$hr = _VirtualDom_node('hr');
var $zaboco$elm_draggable$Draggable$alwaysPreventDefaultAndStopPropagation = function (msg) {
	return {message: msg, preventDefault: true, stopPropagation: true};
};
var $zaboco$elm_draggable$Internal$StartDragging = F2(
	function (a, b) {
		return {$: 'StartDragging', a: a, b: b};
	});
var $zaboco$elm_draggable$Draggable$baseDecoder = function (key) {
	return A2(
		$elm$json$Json$Decode$map,
		A2(
			$elm$core$Basics$composeL,
			$zaboco$elm_draggable$Draggable$Msg,
			$zaboco$elm_draggable$Internal$StartDragging(key)),
		$zaboco$elm_draggable$Draggable$positionDecoder);
};
var $elm$json$Json$Decode$fail = _Json_fail;
var $zaboco$elm_draggable$Draggable$whenLeftMouseButtonPressed = function (decoder) {
	return A2(
		$elm$json$Json$Decode$andThen,
		function (button) {
			if (!button) {
				return decoder;
			} else {
				return $elm$json$Json$Decode$fail('Event is only relevant when the main mouse button was pressed.');
			}
		},
		A2($elm$json$Json$Decode$field, 'button', $elm$json$Json$Decode$int));
};
var $zaboco$elm_draggable$Draggable$mouseTrigger = F2(
	function (key, envelope) {
		return A2(
			$elm$html$Html$Events$custom,
			'mousedown',
			A2(
				$elm$json$Json$Decode$map,
				A2($elm$core$Basics$composeL, $zaboco$elm_draggable$Draggable$alwaysPreventDefaultAndStopPropagation, envelope),
				$zaboco$elm_draggable$Draggable$whenLeftMouseButtonPressed(
					$zaboco$elm_draggable$Draggable$baseDecoder(key))));
	});
var $elm$virtual_dom$VirtualDom$style = _VirtualDom_style;
var $elm$html$Html$Attributes$style = $elm$virtual_dom$VirtualDom$style;
var $elm$svg$Svg$svg = $elm$svg$Svg$trustedNode('svg');
var $author$project$Canvas$ResetInitialState = {$: 'ResetInitialState'};
var $author$project$Canvas$ScalableFactorDown = {$: 'ScalableFactorDown'};
var $author$project$Canvas$ScalableFactorUp = {$: 'ScalableFactorUp'};
var $author$project$Canvas$UpdateFontSize = function (a) {
	return {$: 'UpdateFontSize', a: a};
};
var $elm$html$Html$a = _VirtualDom_node('a');
var $elm$html$Html$li = _VirtualDom_node('li');
var $elm$virtual_dom$VirtualDom$Normal = function (a) {
	return {$: 'Normal', a: a};
};
var $elm$html$Html$Events$on = F2(
	function (event, decoder) {
		return A2(
			$elm$virtual_dom$VirtualDom$on,
			event,
			$elm$virtual_dom$VirtualDom$Normal(decoder));
	});
var $elm$html$Html$Events$onClick = function (msg) {
	return A2(
		$elm$html$Html$Events$on,
		'click',
		$elm$json$Json$Decode$succeed(msg));
};
var $elm$html$Html$span = _VirtualDom_node('span');
var $author$project$Main$toolMenuIcons = _List_fromArray(
	[
		A2(
		$elm$html$Html$li,
		_List_Nil,
		_List_fromArray(
			[
				A2(
				$elm$html$Html$a,
				_List_fromArray(
					[
						A2($elm$html$Html$Attributes$attribute, 'uk-icon', 'icon: refresh'),
						A2($elm$html$Html$Attributes$attribute, 'uk-tooltip', 'title: Reset; pos: left'),
						$elm$html$Html$Events$onClick($author$project$Canvas$ResetInitialState)
					]),
				_List_Nil)
			])),
		A2(
		$elm$html$Html$li,
		_List_Nil,
		_List_fromArray(
			[
				A2(
				$elm$html$Html$a,
				_List_fromArray(
					[
						A2($elm$html$Html$Attributes$attribute, 'uk-tooltip', 'title: Text size down; pos: left'),
						$elm$html$Html$Events$onClick(
						$author$project$Canvas$UpdateFontSize(-1.0))
					]),
				_List_fromArray(
					[
						A2(
						$elm$html$Html$span,
						_List_fromArray(
							[
								A2($elm$html$Html$Attributes$attribute, 'uk-icon', 'icon: triangle-down')
							]),
						_List_fromArray(
							[
								$elm$html$Html$text('123')
							]))
					]))
			])),
		A2(
		$elm$html$Html$li,
		_List_Nil,
		_List_fromArray(
			[
				A2(
				$elm$html$Html$a,
				_List_fromArray(
					[
						A2($elm$html$Html$Attributes$attribute, 'uk-tooltip', 'title: Text size up; pos: left'),
						$elm$html$Html$Events$onClick(
						$author$project$Canvas$UpdateFontSize(1.0))
					]),
				_List_fromArray(
					[
						A2(
						$elm$html$Html$span,
						_List_fromArray(
							[
								A2($elm$html$Html$Attributes$attribute, 'uk-icon', 'icon: triangle-up')
							]),
						_List_fromArray(
							[
								$elm$html$Html$text('123')
							]))
					]))
			])),
		A2(
		$elm$html$Html$li,
		_List_Nil,
		_List_fromArray(
			[
				A2(
				$elm$html$Html$a,
				_List_fromArray(
					[
						A2($elm$html$Html$Attributes$attribute, 'uk-tooltip', 'title: Drawing scale down; pos: left'),
						$elm$html$Html$Events$onClick($author$project$Canvas$ScalableFactorDown)
					]),
				_List_fromArray(
					[
						A2(
						$elm$html$Html$span,
						_List_fromArray(
							[
								A2($elm$html$Html$Attributes$attribute, 'uk-icon', 'icon: shrink')
							]),
						_List_fromArray(
							[
								$elm$html$Html$text('⬤◢')
							]))
					]))
			])),
		A2(
		$elm$html$Html$li,
		_List_Nil,
		_List_fromArray(
			[
				A2(
				$elm$html$Html$a,
				_List_fromArray(
					[
						A2($elm$html$Html$Attributes$attribute, 'uk-tooltip', 'title: Drawing scale up; pos: left'),
						$elm$html$Html$Events$onClick($author$project$Canvas$ScalableFactorUp)
					]),
				_List_fromArray(
					[
						A2(
						$elm$html$Html$span,
						_List_fromArray(
							[
								A2($elm$html$Html$Attributes$attribute, 'uk-icon', 'icon: expand')
							]),
						_List_fromArray(
							[
								$elm$html$Html$text('⬤◢')
							]))
					]))
			]))
	]);
var $elm$html$Html$ul = _VirtualDom_node('ul');
var $author$project$Main$toolMenu = A2(
	$elm$html$Html$ul,
	_List_fromArray(
		[
			$elm$html$Html$Attributes$class('uk-iconnav uk-iconnav-vertical')
		]),
	$author$project$Main$toolMenuIcons);
var $author$project$Canvas$RequestEntities = function (a) {
	return {$: 'RequestEntities', a: a};
};
var $elm$html$Html$Attributes$href = function (url) {
	return A2(
		$elm$html$Html$Attributes$stringProperty,
		'href',
		_VirtualDom_noJavaScriptUri(url));
};
var $author$project$Main$treeMenuItem = function (item) {
	return A2(
		$elm$html$Html$a,
		_List_fromArray(
			[
				$elm$html$Html$Attributes$href('#'),
				$elm$html$Html$Events$onClick(
				$author$project$Canvas$RequestEntities(item.path))
			]),
		_List_fromArray(
			[
				$elm$html$Html$text(item.displayName)
			]));
};
var $author$project$Main$treeMenu = function (model) {
	var labels = A2(
		$elm$core$List$map,
		function (label) {
			return A2(
				$elm$html$Html$li,
				_List_fromArray(
					[
						$elm$html$Html$Attributes$class('uk-parent')
					]),
				_List_fromArray(
					[
						A2(
						$elm$html$Html$a,
						_List_fromArray(
							[
								A2($elm$html$Html$Attributes$attribute, 'href', '#')
							]),
						_List_fromArray(
							[
								$elm$html$Html$text(label.name),
								A2(
								$elm$html$Html$span,
								_List_fromArray(
									[
										A2($elm$html$Html$Attributes$attribute, 'uk-nav-parent-icon', '')
									]),
								_List_Nil)
							])),
						A2(
						$elm$html$Html$ul,
						_List_fromArray(
							[
								$elm$html$Html$Attributes$class('uk-nav-sub')
							]),
						A2(
							$elm$core$List$map,
							function (a) {
								return A2(
									$elm$html$Html$li,
									_List_Nil,
									_List_fromArray(
										[a]));
							},
							A2(
								$elm$core$List$map,
								$author$project$Main$treeMenuItem,
								A2(
									$elm$core$List$filter,
									function (item) {
										return A2(
											$elm$core$List$any,
											function (labelName) {
												return _Utils_eq(labelName, label.name);
											},
											item.labelNames);
									},
									model.tree))))
					]));
		},
		model.labels);
	return A2(
		$elm$html$Html$ul,
		_List_fromArray(
			[
				$elm$html$Html$Attributes$class('uk-nav uk-nav-default'),
				A2($elm$html$Html$Attributes$attribute, 'uk-nav', 'multiple: true')
			]),
		labels);
};
var $author$project$Canvas$ActivatedTag = function (a) {
	return {$: 'ActivatedTag', a: a};
};
var $author$project$Canvas$DeactivatedTag = function (a) {
	return {$: 'DeactivatedTag', a: a};
};
var $elm$html$Html$button = _VirtualDom_node('button');
var $elm$html$Html$h2 = _VirtualDom_node('h2');
var $elm$html$Html$Attributes$id = $elm$html$Html$Attributes$stringProperty('id');
var $elm$html$Html$label = _VirtualDom_node('label');
var $elm$html$Html$Attributes$type_ = $elm$html$Html$Attributes$stringProperty('type');
var $author$project$Main$visibleControlModalId = 'visible-control-modal';
var $author$project$Main$visibleControlModal = function (tags) {
	var targetChecked = A2(
		$elm$json$Json$Decode$at,
		_List_fromArray(
			['target', 'checked']),
		$elm$json$Json$Decode$bool);
	var onCheck = function (tagger) {
		return A2(
			$elm$html$Html$Events$on,
			'change',
			A2($elm$json$Json$Decode$map, tagger, targetChecked));
	};
	var header = A2(
		$elm$html$Html$div,
		_List_fromArray(
			[
				$elm$html$Html$Attributes$class('uk-modal-header')
			]),
		_List_fromArray(
			[
				A2(
				$elm$html$Html$h2,
				_List_Nil,
				_List_fromArray(
					[
						$elm$html$Html$text('Visible Items')
					]))
			]));
	var closeButton = A2(
		$elm$html$Html$button,
		_List_fromArray(
			[
				$elm$html$Html$Attributes$class('uk-modal-close-default'),
				$elm$html$Html$Attributes$type_('button'),
				A2($elm$html$Html$Attributes$attribute, 'uk-close', '')
			]),
		_List_Nil);
	var body = A2(
		$elm$html$Html$div,
		_List_Nil,
		A2(
			$elm$core$List$map,
			function (tag) {
				return A2(
					$elm$html$Html$div,
					_List_fromArray(
						[
							$elm$html$Html$Attributes$class('uk-padding-small')
						]),
					_List_fromArray(
						[
							A2(
							$elm$html$Html$label,
							_List_Nil,
							_List_fromArray(
								[
									A2(
									$elm$html$Html$div,
									_List_fromArray(
										[
											$elm$html$Html$Attributes$class(tag.key)
										]),
									_List_fromArray(
										[
											A2(
											$elm$html$Html$button,
											_List_fromArray(
												[
													$elm$html$Html$Attributes$type_('button'),
													$elm$html$Html$Attributes$class('uk-margin-right'),
													A2($elm$html$Html$Attributes$attribute, 'uk-icon', 'icon: eye'),
													A2($elm$html$Html$Attributes$attribute, 'uk-toggle', 'target: .' + tag.key),
													onCheck(
													function (_v0) {
														return $author$project$Canvas$ActivatedTag(tag.key);
													})
												]),
											_List_Nil),
											A2(
											$elm$html$Html$span,
											_List_fromArray(
												[
													A2($elm$html$Html$Attributes$style, 'color', 'black'),
													A2($elm$html$Html$Attributes$style, 'font-weight', 'bold')
												]),
											_List_fromArray(
												[
													$elm$html$Html$text(tag.displayName)
												]))
										])),
									A2(
									$elm$html$Html$div,
									_List_fromArray(
										[
											$elm$html$Html$Attributes$class(tag.key),
											A2($elm$html$Html$Attributes$attribute, 'hidden', '')
										]),
									_List_fromArray(
										[
											A2(
											$elm$html$Html$button,
											_List_fromArray(
												[
													$elm$html$Html$Attributes$type_('button'),
													$elm$html$Html$Attributes$class('uk-margin-right'),
													A2($elm$html$Html$Attributes$attribute, 'uk-icon', 'icon: eye-slash'),
													A2($elm$html$Html$Attributes$attribute, 'uk-toggle', 'target: .' + tag.key),
													onCheck(
													function (_v1) {
														return $author$project$Canvas$DeactivatedTag(tag.key);
													})
												]),
											_List_Nil),
											A2(
											$elm$html$Html$span,
											_List_fromArray(
												[
													A2($elm$html$Html$Attributes$style, 'color', 'gray')
												]),
											_List_fromArray(
												[
													$elm$html$Html$text(tag.displayName)
												]))
										]))
								]))
						]));
			},
			tags));
	return A2(
		$elm$html$Html$div,
		_List_fromArray(
			[
				$elm$html$Html$Attributes$id($author$project$Main$visibleControlModalId),
				A2($elm$html$Html$Attributes$attribute, 'uk-modal', '')
			]),
		_List_fromArray(
			[
				A2(
				$elm$html$Html$div,
				_List_fromArray(
					[
						$elm$html$Html$Attributes$class('uk-modal-dialog uk-padding')
					]),
				_List_fromArray(
					[closeButton, header, body]))
			]));
};
var $author$project$Main$visibleControlPanel = function (tags) {
	return A2(
		$elm$html$Html$div,
		_List_Nil,
		A2(
			$elm$core$List$map,
			function (tag) {
				return A2(
					$elm$html$Html$div,
					_List_Nil,
					_List_fromArray(
						[
							A2(
							$elm$html$Html$label,
							_List_Nil,
							_List_fromArray(
								[
									A2(
									$elm$html$Html$div,
									_List_fromArray(
										[
											$elm$html$Html$Attributes$class(tag.key)
										]),
									_List_fromArray(
										[
											A2(
											$elm$html$Html$button,
											_List_fromArray(
												[
													$elm$html$Html$Attributes$type_('button'),
													$elm$html$Html$Attributes$class('uk-margin-right'),
													A2($elm$html$Html$Attributes$attribute, 'uk-icon', 'icon: eye'),
													A2($elm$html$Html$Attributes$attribute, 'uk-toggle', 'target: .' + tag.key),
													$elm$html$Html$Events$onClick(
													$author$project$Canvas$DeactivatedTag(tag.key))
												]),
											_List_Nil),
											A2(
											$elm$html$Html$span,
											_List_fromArray(
												[
													A2($elm$html$Html$Attributes$style, 'color', 'black'),
													A2($elm$html$Html$Attributes$style, 'font-weight', 'bold')
												]),
											_List_fromArray(
												[
													$elm$html$Html$text(tag.displayName)
												]))
										])),
									A2(
									$elm$html$Html$div,
									_List_fromArray(
										[
											$elm$html$Html$Attributes$class(tag.key),
											A2($elm$html$Html$Attributes$attribute, 'hidden', '')
										]),
									_List_fromArray(
										[
											A2(
											$elm$html$Html$button,
											_List_fromArray(
												[
													$elm$html$Html$Attributes$type_('button'),
													$elm$html$Html$Attributes$class('uk-margin-right'),
													A2($elm$html$Html$Attributes$attribute, 'uk-icon', 'icon: eye-slash'),
													A2($elm$html$Html$Attributes$attribute, 'uk-toggle', 'target: .' + tag.key),
													$elm$html$Html$Events$onClick(
													$author$project$Canvas$ActivatedTag(tag.key))
												]),
											_List_Nil),
											A2(
											$elm$html$Html$span,
											_List_fromArray(
												[
													A2($elm$html$Html$Attributes$style, 'color', 'gray'),
													A2($elm$html$Html$Attributes$style, 'font-weight', 'bold')
												]),
											_List_fromArray(
												[
													$elm$html$Html$text(tag.displayName)
												]))
										]))
								]))
						]));
			},
			tags));
};
var $author$project$Main$view = function (model) {
	var entities = model.entities;
	var drawingObjects = $author$project$Canvas$drawModel(model);
	var converter = $author$project$Canvas$getCoordinateConverter(model);
	var scaleFactor = $author$project$Canvas$computeScaleFactor(converter);
	var valueBound = converter.valueBounding;
	var valueRangeX = valueBound.maxX - valueBound.minX;
	var valueRangeY = valueBound.maxY - valueBound.minY;
	var boundY = 'boundY(' + ($elm$core$String$fromFloat(valueBound.minY) + (', ' + ($elm$core$String$fromFloat(valueBound.maxY) + ')')));
	var boundX = 'boundX(' + ($elm$core$String$fromFloat(valueBound.minX) + (', ' + ($elm$core$String$fromFloat(valueBound.maxX) + ')')));
	var _v0 = model.config;
	var centerX = _v0.centerX;
	var centerY = _v0.centerY;
	var width = _v0.width;
	var height = _v0.height;
	var zoom = _v0.zoom;
	var zooming = 'scale(' + ($elm$core$String$fromFloat(zoom * scaleFactor) + ')');
	var _v1 = _Utils_Tuple2(((width / zoom) / scaleFactor) / 2, ((height / zoom) / scaleFactor) / 2);
	var halfWidth = _v1.a;
	var halfHeight = _v1.b;
	var _v2 = _Utils_Tuple2(centerX, centerY);
	var cx = _v2.a;
	var cy = _v2.b;
	var _v3 = _Utils_Tuple2(cy - halfHeight, cx - halfWidth);
	var top = _v3.a;
	var left = _v3.b;
	var panning = 'translate(' + ($elm$core$String$fromFloat(-left) + (', ' + ($elm$core$String$fromFloat(-top) + ')')));
	var debugContent = A2(
		$elm$html$Html$div,
		_List_Nil,
		_List_fromArray(
			[
				$elm$html$Html$text(panning),
				$elm$html$Html$text(zooming),
				$elm$html$Html$text(boundX),
				$elm$html$Html$text(boundY)
			]));
	var _v4 = _Utils_Tuple2(cy + halfHeight, cx + halfWidth);
	var bottom = _v4.a;
	var right = _v4.b;
	var descriptions = A2(
		$elm$core$List$indexedMap,
		F2(
			function (i, description) {
				var y = (i + 1) * 30;
				var x = right - 40.0;
				return A2(
					$elm$svg$Svg$text_,
					_List_fromArray(
						[
							A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x, x),
							A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y, y),
							$elm$svg$Svg$Attributes$textAnchor('end'),
							$elm$svg$Svg$Attributes$dominantBaseline('text-after-edge')
						]),
					_List_fromArray(
						[
							$elm$html$Html$text(description)
						]));
			}),
		model.config.descriptions);
	var _v5 = model.config;
	var contourMax = _v5.contourMax;
	var contourMin = _v5.contourMin;
	var _v6 = model.config;
	var fontSize = _v6.fontSize;
	var visibleColorBar = _v6.visibleColorBar;
	var colorBarX = _v6.colorBarX;
	var colorBarY = _v6.colorBarY;
	var colorBar = visibleColorBar ? A2(
		$elm$core$List$append,
		_List_fromArray(
			[
				A2(
				$elm$svg$Svg$text_,
				_List_fromArray(
					[
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x, colorBarX + 20),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y, colorBarY),
						$elm$svg$Svg$Attributes$textAnchor('end'),
						$elm$svg$Svg$Attributes$dominantBaseline('text-after-edge')
					]),
				_List_fromArray(
					[
						$elm$html$Html$text(
						$elm$core$String$fromFloat(contourMax))
					])),
				A2(
				$elm$svg$Svg$text_,
				_List_fromArray(
					[
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x, colorBarX + 20),
						A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y, colorBarY + 256),
						$elm$svg$Svg$Attributes$textAnchor('end'),
						$elm$svg$Svg$Attributes$dominantBaseline('text-before-edge')
					]),
				_List_fromArray(
					[
						$elm$html$Html$text(
						$elm$core$String$fromFloat(contourMin))
					]))
			]),
		A2(
			$elm$core$List$map,
			function (_v8) {
				var i = _v8.a;
				var color = _v8.b;
				var _v9 = color;
				var r = _v9.a;
				var g = _v9.b;
				var b = _v9.c;
				var colorCss = $avh4$elm_color$Color$toCssString(
					A3($avh4$elm_color$Color$rgb, r, g, b));
				return A2(
					$elm$svg$Svg$rect,
					_List_fromArray(
						[
							A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$x, colorBarX),
							A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$y, colorBarY + i),
							A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$width, 20),
							A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$height, 5),
							$elm$svg$Svg$Attributes$fill(colorCss),
							$elm$svg$Svg$Attributes$stroke(colorCss),
							A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$strokeWidth, 1)
						]),
					_List_Nil);
			},
			A2(
				$elm$core$List$filter,
				function (_v7) {
					var i = _v7.a;
					return !(i % 5);
				},
				A2(
					$elm$core$List$indexedMap,
					F2(
						function (i, color) {
							return _Utils_Tuple2(i, color);
						}),
					$elm$core$List$reverse($author$project$Canvas$turboColormapData))))) : _List_Nil;
	var mainContent = A2(
		$elm$html$Html$div,
		_List_fromArray(
			[
				A2($elm$html$Html$Attributes$style, 'text-align', 'left'),
				A2($elm$html$Html$Attributes$style, 'margin', '0 auto')
			]),
		_List_fromArray(
			[
				A2(
				$elm$html$Html$div,
				_List_fromArray(
					[
						A2($elm$html$Html$Attributes$attribute, 'uk-grid', '')
					]),
				_List_fromArray(
					[
						A2(
						$elm$html$Html$div,
						_List_fromArray(
							[
								$elm$html$Html$Attributes$class('uk-width-1-6')
							]),
						_List_fromArray(
							[
								$author$project$Main$treeMenu(model)
							])),
						A2(
						$elm$html$Html$div,
						_List_fromArray(
							[
								$elm$html$Html$Attributes$class('uk-width-expand')
							]),
						_List_fromArray(
							[
								A2(
								$elm$svg$Svg$svg,
								_List_fromArray(
									[
										A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$width, width),
										A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$height, height),
										A2($elm$html$Html$Attributes$style, 'margin', '0 auto'),
										$author$project$Canvas$handleZoom($author$project$Canvas$Zoom),
										A2($zaboco$elm_draggable$Draggable$mouseTrigger, _Utils_Tuple0, $author$project$Canvas$DragMsg)
									]),
								A2(
									$elm$core$List$append,
									_List_fromArray(
										[
											$author$project$Canvas$background,
											A2(
											$elm$svg$Svg$g,
											_List_fromArray(
												[
													$elm$svg$Svg$Attributes$transform(zooming + (' ' + panning)),
													$elm$svg$Svg$Attributes$stroke('black'),
													$elm$svg$Svg$Attributes$fill('none'),
													A2($author$project$Canvas$num, $elm$svg$Svg$Attributes$fontSize, fontSize)
												]),
											drawingObjects)
										]),
									$elm$core$List$concat(
										_List_fromArray(
											[colorBar, descriptions]))))
							])),
						A2(
						$elm$html$Html$div,
						_List_fromArray(
							[
								A2($elm$html$Html$Attributes$style, 'position', 'fixed'),
								A2($elm$html$Html$Attributes$style, 'right', '20px')
							]),
						_List_fromArray(
							[
								$author$project$Main$toolMenu,
								A2(
								$elm$html$Html$hr,
								_List_fromArray(
									[
										$elm$html$Html$Attributes$class('uk-divider-small')
									]),
								_List_Nil),
								$author$project$Main$visibleControlPanel(model.tags)
							]))
					]))
			]));
	return A2(
		$elm$html$Html$div,
		_List_Nil,
		_List_fromArray(
			[
				A2(
				$elm$html$Html$div,
				_List_Nil,
				_List_fromArray(
					[
						mainContent,
						$author$project$Main$visibleControlModal(model.tags)
					]))
			]));
};
var $author$project$Main$main = $elm$browser$Browser$element(
	{init: $author$project$Canvas$init, subscriptions: $author$project$Canvas$subscriptions, update: $author$project$Canvas$update, view: $author$project$Main$view});
_Platform_export({'Main':{'init':$author$project$Main$main($elm$json$Json$Decode$value)(0)}});}(this));