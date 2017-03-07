/**
 * Created by jiaotao on 2017/2/27.
 */


KindEditor.ready(function(K) {
	K.create('textarea[name="content"]', {
		width : "800px",
        height : "200px",
		uploadJson: '/admin/upload/kindeditor',
	});
});