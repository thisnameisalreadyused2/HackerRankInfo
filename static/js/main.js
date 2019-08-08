let data;
$.getJSON('http://127.0.0.1:5000/team/1-thisnameisalreadyused2/statistics', function(json) {
    data = json;
});

function getRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}


function getLabels(data) {
	// Key is the left-hand string of an object literal ( {...} ).
  // Object.keys({ "a": 1, "b": 2 } will return ["a", "b"]
  // .map returns an array, executing function on every element of an input array.
  // Here we split, i.e. "2019-06-27 12:43:27.038194", by " " and get the first substring.
    console.log(Object.keys(data));
	return Object.keys(data).map((v) => { return v.split(' ')[0] });
  // Can be simplified to:
  // return Object.keys(data).map(v => v.split(' ')[0]);
}

function extractData(data) {
	// We need to transform each user's record to this form (result will be an array of such objects):
  // { userId: 1, score: [ 287, 316 ] }
  // WARN: for this method to work as expected, dates in input object should be sorted chronologically

  // Prepare an array of user id's to use as an index map for the resulting array
  // Index of user id in this array will be equal to their object in resulting array
  // I.e.: userIds = [ 100, 200 ], so resultArray = [ { userId: 100, ... }, { userId: 200, ... } ]
  const userIds = [];
  const resultArray = [];
  for (const date of Object.keys(data)) {
  	// date stores "2019-06-27 12:43:27.038194", "2019-07-01 21:15:32.462196", so we can access object's values like this:
    const dayData = data[date];
    if (!dayData) continue;

    for (const record of dayData) {
    	// record = { "score": 193, "user_id": 454355 }
      const idIndex = userIds.indexOf(record.user_id);
    	if (idIndex >= 0) {
				// User's object exists in resulting array, just add their score to "score" array
        resultArray[idIndex].score.push(record.score)
			} else {
      	// This user was seen for the first time, need to create their object
        userIds.push(record.user_id);
        resultArray.push({
        	userId: "User " + record.user_id,
          score: [ record.score ] // Our first score in array (first point on plot for this user)
        });
      }
    }
  }

  return resultArray;
}

function prepareChartDatasets(data) {
	return data.map(v => {
  	const randomColor = getRandomColor();

    return {
      label: v.userId,
      backgroundColor: randomColor,
      borderColor: randomColor,
      data: v.score,
   		fill: false,
    };
  })
}

let cfg = {
  type: 'line',
  data: {
    labels: getLabels(data),
    datasets: prepareChartDatasets(extractData(data)),
  },
  options: {
    responsive: true,
    title: {
      display: true,
      text: 'Score Chart'
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true
    },
    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Date'
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Score'
        }
      }]
    }
  }
};

setTimeout(function() {
	let ctx = document.getElementById('canvas').getContext('2d');
	window.myLine = new Chart(ctx, cfg);
	console.log(data);
	window.myLine.update();
}, 2000);