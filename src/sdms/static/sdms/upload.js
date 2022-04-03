var isAdvancedUpload = function() {
  var div = document.createElement('div');
  return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
}();

window.onload = function ()
{
	var form = document.getElementById("ulform");
	if (isAdvancedUpload) {
	  form.className = 'ulform has-advanced-upload';

	  form.ondragover = form.ondragenter = function(e) {
	  	e.preventDefault();
    	e.stopPropagation();
	  	form.className = 'ulform has-advanced-upload isdragover';
	  };

	  form.ondragleave = form.ondragend = function(e) {
	  	e.preventDefault();
    	e.stopPropagation();
	  	form.className = 'ulform has-advanced-upload';
	  };

	  form.ondrag = form.ondragstart = function (e) {
	  	e.preventDefault();
    	e.stopPropagation();
	  };

	  form.ondrop = function (e) {
	  	e.preventDefault();
    	e.stopPropagation();
	  	form.className = 'ulform has-advanced-upload';
      var fileinput = document.getElementById("file");
      fileinput.files = e.dataTransfer.files;
	  	form.submit();
	  };
	}
};
