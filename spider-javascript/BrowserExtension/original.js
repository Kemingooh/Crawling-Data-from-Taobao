
// 模拟鼠标点击

function simulateMouseClick(targetNode) {
    if (!targetNode) {
        alert('element not found!')
        throw 'element not found'
    }
    function triggerMouseEvent(eventType) {
        var clickEvent = document.createEvent('MouseEvents');
        clickEvent.initEvent(eventType, true, true);
        targetNode.dispatchEvent(clickEvent);
    }
    ["mouseover", "mousedown", "mouseup", "click"].forEach(triggerMouseEvent);
}


// 随机休息(base, base * 2)毫秒，之后调用next
function randomSleep(next, base) {
    base = base || 5000;
    setTimeout(next, base + Math.random() * base)
}


// 处理商品详情页面
function handleItemPage() {
    var itemUrl = location.href
    var itemID = (itemUrl.split('id=')[1]).split('&')[0]
    var pro_info
    var original_num = document.getElementById('J_StrPrice').innerText
    var promoPriceNum = document.getElementById('J_PromoPriceNum')
    var current_num = ''

    if (promoPriceNum) {
        current_num = promoPriceNum.innerText
    }

    var sellcounter = document.getElementById('J_SellCounter').innerText
    var Taocoin = document.getElementById('J_OtherDiscount').innerText
    var from = document.getElementById('J_From').innerText
    var popularity = document.getElementById('J_Social').innerText
    var delivery = document.getElementById('J_WlServiceTitle').innerText
    var commitments = document.getElementById('J_tbExtra').children[0].getElementsByTagName('a')
    var commitmentString = ''
    for (var i = 0; i < commitments.length; i++) {
        var commitment = commitments[i]
        commitmentString += commitment.innerText
        if (i < commitments.length - 1) {
            commitmentString += ','
        }
    }

    pro_info = ['PRODINFO', original_num, current_num, sellcounter, Taocoin, from, popularity, delivery, commitmentString]
    content.fetch('http://127.0.0.1:8710/api', {
        method: 'post',
        body: JSON.stringify([pro_info])
    }).then(() => {
        console.log('fetch done')
    })

    // 点击“评价”标签
    simulateMouseClick(document.getElementsByClassName('J_ReviewsCount')[0])
    // 当前的页面（假定一开始是第一页）
    var currentPage = 1

    // 用于分析当前评价页面，并自动切换到下一页的函数
    function handleCommentPage() {
        // 获取本页所有评论
        var comments = document.getElementsByClassName('J_KgRate_ReviewItem')
        var arr = []
        for (var i = 0; i < comments.length; i++) {
            var comment = comments[i]
            // 评论ID
            var commentID = comment.id
            // 评论日期
            var commentDate = comment.getElementsByClassName('tb-r-date')[0].innerText
            // 评论内容
            var commentContent = comment.getElementsByClassName('tb-tbcr-content')[0].innerText
            console.log(commentID, commentDate, commentContent)
            arr.push([itemID, currentPage, commentID, commentDate, commentContent])
        }
        // 转换为JSON后，调用server.py
        console.log('fetch start')
        content.fetch('http://127.0.0.1:8710/api', {
            method: 'post',
            body: JSON.stringify(arr)
        }).then(() => {
            console.log('fetch done')
        })

        // 查找评论的“下一页”按钮
        var pgNext = document.getElementsByClassName('pg-next')[0]
        // 如果“下一页”按钮被禁用，说明已经到达最后一页
        var allPagesDone = ('' + pgNext.className).indexOf('disable') >= 0
        // 如果超过了100页也停止爬取
        if (currentPage >= 100) {
            allPagesDone = true
        }
        if (!allPagesDone) {
            currentPage++
            // 点击“下一页”按钮
            simulateMouseClick(document.getElementsByClassName('pg-next')[0])
            // 随机等待后调用分析函数
            randomSleep(() => {
                handleCommentPage()
            }, 3000)
        } else {
            alert('all pages done!')
        }
    }

    // 随机等待后点击“按时间排序”
    randomSleep(() => {
        simulateMouseClick(document.getElementsByClassName('ico-sort-by-time')[0])
        // 随机等待后调用分析函数
        randomSleep(() => {
            handleCommentPage()
        }, 3000)
    }, 3000)
}



try {
    // 是否是商品详情页面？
    if (location.href.indexOf('/item.htm') > 0) {
        // taobao item page
        randomSleep(handleItemPage, 5000)
    }

} catch (error) {
    console.log(error)
}


/*


https://item.taobao.com/item.htm?id=580689308613



*/


/*
var arr
var currentPos
function handleItemList() {
    arr = document.getElementsByClassName('item-name')
    currentPos = 0
    var items = []
    for (var i = 0; i < arr.length; i++) {
        items.push({
            'url': arr[i].href
        })
    }
    browser.runtime.sendMessage({
        type: 'item-list',
        items: items
    })
    clickOneItem()
}

function clickOneItem() {
    if (currentPos >= arr.length) {
        var e = document.getElementsByClassName('next')
        if (e.length > 0) {
            e[0].click()
        }
        return
    }
    simulateMouseClick(arr[currentPos])
    currentPos++
    setTimeout(clickOneItem, 5000 + Math.random() * 5000)
}

if (location.href.indexOf('search.htm?') >= 0) {
    setTimeout(handleItemList, 5000)
}*/




