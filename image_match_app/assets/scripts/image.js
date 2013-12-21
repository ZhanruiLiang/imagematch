var prePageNum = 0;

var Config = {
    ImagesPerPage: 10,
    ImageURLBasePath: 'image/',
    ImageIdPrefix: 'result-img-',
    AlwaysShowInfo: true,
};

var nImages = searchResults.length;
var nPages = Math.ceil(nImages / Config.ImagesPerPage);

function showImages(pageNum) {
    // 显示搜索结果，静态页面下图片id与文件名相同
    var imgs = '';
    for (var i = pageNum * Config.ImagesPerPage + 0; i < (pageNum + 1) * Config.ImagesPerPage && i < nImages; i++) {
        var path = Config.ImageURLBasePath + searchResults[i][0];
        var rate = searchResults[i][1];
        var img = '<li onmouseover="imgInfoHover(' + i 
            + ')" onmouseout="imgInfoMouseOut(' + i + ')"><img id="' + Config.ImageIdPrefix + i.toString() 
            + '" src="' + path 
            + '" alt="' + searchResults[i][0]
            + '"></img><span class="' + (Config.AlwaysShowInfo ? "imginfo-hover" : "imginfo") 
            + '">Likelyhood: ' + rate
            + '</span></li>\n';
        imgs += img;
    };
    document.getElementById('images-ul').innerHTML = imgs;
}

function pagination() {
    // 显示分页DIV
    var html = '<a id="prePage" onclick="goPrePage()"><li>&lt;</li></a>';
    html += '<a id="page0" onclick="goPage(0)" class="selected"><li>1</li></a>';
    for (var i = 1; i < nPages; i++) {
        var li = '<a id="page' + i.toString() + '\" onclick="goPage(' + i.toString() + ')"><li>' + (i + 1).toString() + '</li></a>';
        html += li;
    };
    html += '<a id="nextPage" onclick="goNextPage()"><li>&gt;</li></a>';
    document.getElementById('pagination-ul').innerHTML = html;
}

function goPage(pageNum) {
    // 在分页DIV中点击数字跳转页面
    var page = document.getElementById('page' + pageNum.toString());
    page.className = "selected";
    showImages(pageNum);
    hideSwitcher(pageNum);
    if (prePageNum != pageNum) {
        var prePage = document.getElementById('page' + prePageNum.toString());
        prePage.className = '';
    }
    prePageNum = pageNum;
}

function goPrePage() {
    // 跳转至前一页
    if (prePageNum > 0)
        var pageNum = prePageNum - 1;
    goPage(pageNum);
}

function goNextPage() {
    // 跳转至后一页
    if (prePageNum < nPages - 1)
        var pageNum = prePageNum + 1;
    goPage(pageNum);
}

function hideSwitcher(pageNum) {
    // 在第一页和最后一页是隐藏左右Switcher
    document.getElementById('pre').style.display = (pageNum == 0 ? 'none' : 'block');
    document.getElementById('next').style.display = (pageNum == nPages - 1 ? 'none' : 'block');
}

function imgInfoHover(id) {
    if(!Config.AlwaysShowInfo) {
        // 在鼠标停留在图片上时，显示 Hash Distance 
        imgInfo = document.getElementById(Config.ImageIdPrefix + id).parentNode.lastChild;
        imgInfo.className = 'imginfo-hover';
    }
}

function imgInfoMouseOut(id) {
    if(!Config.AlwaysShowInfo) {
        // 在鼠标离开图片时，隐藏 Hash Distance 
        imgInfo = document.getElementById(Config.ImageIdPrefix + id).parentNode.lastChild;
        imgInfo.className = 'imginfo';
    }
}

showImages(0);
pagination();
