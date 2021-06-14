from suggestions import getSugsFromFile
from flask import Flask, render_template, request

app = Flask(__name__)

se_apis = { 
				'qwant':'https://api.qwant.com/api/suggest/?q={}',
				'duckduckgo':'https://duckduckgo.com/ac/?q={}',
				'google':'https://suggestqueries.google.com/complete/search?client=firefox&q={}',		
				'amazon':'http://completion.amazon.com/search/complete?{}&client=amazon-search-ui&mkt=1&q={}',
			}

@app.route('/')
def index_page():
	return render_template('index.html', suggestions=[])

@app.route('/launch', methods=['GET','POST'])
def launch():
	print("\nLAUNCHED!\n")
	input_keyword = request.form['keyword']
	amazon_department = request.form['amazon_department']

	api_urls = se_apis.copy()
	api_urls['amazon'] = api_urls['amazon'].format(amazon_department, input_keyword)
	
	i = 0
	suggestions = [ 1 for e in se_apis ]
	for engine in api_urls:
		
		engine_results = set()
	
		for result in getSugsFromFile(api_urls[engine], input_keyword):
			engine_results.add(result)
		print(engine, engine_results)

		suggestions[i] = engine_results
		i+=1
	
	return render_template('index.html', suggestions=suggestions)


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)