<template lang="html">
    <div v-if="status" id="body-left" class="html-body" key="1">
        <BlogToc :toc="toc"></BlogToc>
        <div class="body-left">
            <div class="blog">
                <div class="blog-head">
                    <h1>
                        <a >{{ detail.title }}</a>
                    </h1>
                </div>
                <div class="blog-info">
                    <span><a href="#">&nbsp;{{ detail.category }}&nbsp;</a></span>
                    <span><a href="#">&nbsp;{{ detail.author }}&nbsp;</a></span>
                    <span>&nbsp;{{ detail.create_time }}&nbsp;</span>
                    <span>&nbsp;{{ detail.views }} 阅读&nbsp;</span>
                </div>
                <div class="markdown-body entry-content" v-html="detail.html"></div>
            </div>
            <div style="height: 100%">
                <Comment :blogid="blogid"></Comment>
            </div>
        </div>
    </div>
</template>

<script type="text/javascript">
    import BlogToc from '../components/BlogToc'
    import Comment from '../components/Comment'
    import Footer from '../components/Footer'
    export default{
        name:"blogdetail",
        components:{
            BlogToc,
            Comment,
            Footer
        },
        data(){
            return{
                detail:[],
                toc:"",
                blogid: "",
                status: false,
            }
        },
        mounted(){
            //window.addEventListener('scroll', this.scrollToTop)
            this.blogid = this.$route.params.id
            this.ShowDetail()
        },
        watch:{
            $route(){
                this.blogid = this.$route.params.id
                this.ShowDetail()
            }
        },
        destroyed(){
            //window.removeEventListener('scroll', this.scrollToTop)
        },
        methods:{
            scrollToTop(){
                var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
                console.log(scrollTop)
            },
            // 获取博文内容
            ShowDetail(){
                //加载
                const loading = this.$loading({
                    lock: true,
                    tagget: 'body-left',
                    text: 'Loading',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0,0,0,0.7)'
                });
                console.log(this.blogid)
                var asd = this.blogid
                console.log(this.GLOBAL.BLOGVIEW)
                if (this.GLOBAL.CountNum(this.blogid)){
                    var blogview = this.HOST + 'countview'
                    this.$axios({
                        method: 'post',
                        url: blogview,
                        params: {
                            id: this.blogid
                        }
                    })
                    .then(res => {
                        console.log('博文加一',this.blogid,res.data.status)
                    })
                    .catch(error => {
                        console.log(error)
                    })
                }
                var url = this.HOST + "blog";
                this.$axios.get(url, {
                    params:{
                        id: this.blogid,
                    }
                })
                .then(res => {
                    if (res.data.status == 0){
                        var blog = res.data.data;
                        var result = blog.html.match(/(<div class="toc">(?:.|\n)*<\/ul>\n<\/div>)/);
                        if (result != null){
                            this.toc = result[0]
                        } else {
                            this.toc = ""
                        }
                        blog.html = blog.html.replace(/(<div class="toc">(?:.|\n)*<\/ul>\n<\/div>)/, "");
                        this.detail = blog;
                    }
                    loading.close()
                    this.status = true
                })
                .catch(error => {
                    console.log(error);
                    loading.close()
                    this.status = true
                })
            }
        }
    }
</script>

<style type="text/css">
    .html-body{
        padding: 0 3%;
        margin: 0 1%;
        margin-top: 80px;
        margin-bottom: 50px;
        flex: 1;
    }
    @media (min-width: 800px){
        .body-left{
            float: left;
            width: 65%;
        }
    }
    @media (max-width: 800px){
        .body-left{
            width: 100%;
            margin: 0 auto;
            max-width: 700px;
            padding-bottom: 30px;
        }
    }
    .blog {
        background-color: #d8d4d473 !important;
        width: 100%;
        margin-bottom: 35px;
    }
    .blog-head {
        padding-top: 20px;
        padding-bottom: 10px;
    }
    .blog-head h1 {
        text-align: center;
    }
    .blog-head h1 a{
        text-decoration:none;
        color: #0b445b;
    }
    .blog-info {
        text-align: center;
        padding-top: 10px;
        padding-bottom:20px;
    }
    .blog-info span{
        background-color: #3D4450;
        color: #FFFFFF;
    }
    .blog-info span a{
        text-decoration:none;
        color: #FFFFFF;
    }
    .entry-content {
        line-height: 1.5;
        padding: 0 20px;
        color: #000;
        word-wrap:break-word;
        word-break:break-all;
        overflow: hidden;
    }
    .entry-content a{
        text-decoration:none;
    }
    .entry-content p{text-indent:2em;}
    .markdown-body table tr {
        background-color: #ababab;
    }
    .markdown-body table tr:nth-child(2n){
        background-color: #ababab;
    }
    .markdown-body img{
        cursor: pointer;
        transition: all 0.6s;
    }
    .markdown-body img:hover{
        transform: scale(1.05);
    }
    .reply-input .el-textarea__inner{
        /*background-color: #8d8d8e;*/
    }
    .entry-content code{
        color: red;
    }
/* CODE
=============================================================================*/

pre, code, tt {
  font-size: 12px;
  font-family: Consolas, "Liberation Mono", Courier, monospace;
}

code, tt {
  margin: 0 0px;
  padding: 0px 0px;
  white-space: nowrap;
  border: 1px solid #eaeaea;
  background-color: #f8f8f8;
  border-radius: 3px;
}

pre>code {
  margin: 0;
  padding: 0;
  white-space: pre;
  border: none;
  background: transparent;
}

pre {
  background-color: #f8f8f8;
  border: 1px solid #ccc;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 6px 0;
  padding-left: 28px;
  border-radius: 3px;
}

pre code, pre tt {
  background-color: transparent;
  border: none;
}

kbd {
    -moz-border-bottom-colors: none;
    -moz-border-left-colors: none;
    -moz-border-right-colors: none;
    -moz-border-top-colors: none;
    background-color: #DDDDDD;
    background-image: linear-gradient(#F1F1F1, #DDDDDD);
    background-repeat: repeat-x;
    border-color: #DDDDDD #CCCCCC #CCCCCC #DDDDDD;
    border-image: none;
    border-radius: 2px 2px 2px 2px;
    border-style: solid;
    border-width: 1px;
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    line-height: 10px;
    padding: 1px 4px;
}

/* QUOTES
=============================================================================*/

blockquote {
  border-left: 4px solid #DDD;
  padding: 0 10px;
  color: #777;
}

blockquote>:first-child {
  margin-top: 0px;
}

blockquote>:last-child {
  margin-bottom: 0px;
}

.codehilite .hll { background-color: #ffffcc }
.codehilite  { background: #f8f8f8; }
.codehilite .c { color: #408080; font-style: italic } /* Comment */
.codehilite .err { border: 1px solid #FF0000 } /* Error */
.codehilite .k { color: #008000; font-weight: bold } /* Keyword */
.codehilite .o { color: #666666 } /* Operator */
.codehilite .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.codehilite .cp { color: #BC7A00 } /* Comment.Preproc */
.codehilite .c1 { color: #408080; font-style: italic } /* Comment.Single */
.codehilite .cs { color: #408080; font-style: italic } /* Comment.Special */
.codehilite .gd { color: #A00000 } /* Generic.Deleted */
.codehilite .ge { font-style: italic } /* Generic.Emph */
.codehilite .gr { color: #FF0000 } /* Generic.Error */
.codehilite .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.codehilite .gi { color: #00A000 } /* Generic.Inserted */
.codehilite .go { color: #808080 } /* Generic.Output */
.codehilite .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.codehilite .gt { color: #0040D0 } /* Generic.Traceback */
.codehilite .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.codehilite .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.codehilite .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.codehilite .kp { color: #008000 } /* Keyword.Pseudo */
.codehilite .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.codehilite .kt { color: #B00040 } /* Keyword.Type */
.codehilite .m { color: #666666 } /* Literal.Number */
.codehilite .s { color: #BA2121 } /* Literal.String */
.codehilite .na { color: #7D9029 } /* Name.Attribute */
.codehilite .nb { color: #008000 } /* Name.Builtin */
.codehilite .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.codehilite .no { color: #880000 } /* Name.Constant */
.codehilite .nd { color: #AA22FF } /* Name.Decorator */
.codehilite .ni { color: #999999; font-weight: bold } /* Name.Entity */
.codehilite .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.codehilite .nf { color: #0000FF } /* Name.Function */
.codehilite .nl { color: #A0A000 } /* Name.Label */
.codehilite .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.codehilite .nt { color: #008000; font-weight: bold } /* Name.Tag */
.codehilite .nv { color: #19177C } /* Name.Variable */
.codehilite .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.codehilite .w { color: #bbbbbb } /* Text.Whitespace */
.codehilite .mf { color: #666666 } /* Literal.Number.Float */
.codehilite .mh { color: #666666 } /* Literal.Number.Hex */
.codehilite .mi { color: #666666 } /* Literal.Number.Integer */
.codehilite .mo { color: #666666 } /* Literal.Number.Oct */
.codehilite .sb { color: #BA2121 } /* Literal.String.Backtick */
.codehilite .sc { color: #BA2121 } /* Literal.String.Char */
.codehilite .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.codehilite .s2 { color: #BA2121 } /* Literal.String.Double */
.codehilite .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.codehilite .sh { color: #BA2121 } /* Literal.String.Heredoc */
.codehilite .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.codehilite .sx { color: #008000 } /* Literal.String.Other */
.codehilite .sr { color: #BB6688 } /* Literal.String.Regex */
.codehilite .s1 { color: #BA2121 } /* Literal.String.Single */
.codehilite .ss { color: #19177C } /* Literal.String.Symbol */
.codehilite .bp { color: #008000 } /* Name.Builtin.Pseudo */
.codehilite .vc { color: #19177C } /* Name.Variable.Class */
.codehilite .vg { color: #19177C } /* Name.Variable.Global */
.codehilite .vi { color: #19177C } /* Name.Variable.Instance */
.codehilite .il { color: #666666 } /* Literal.Number.Integer.Long */
</style>