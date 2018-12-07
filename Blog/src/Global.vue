<script type="text/javascript">
    var INDEX = 0
    var BLOGVIEW = {}
    function CountNum(blogid){
        console.log('global',blogid)
        if (BLOGVIEW[blogid]){
            return false
        } else {
            BLOGVIEW[blogid] = 1
            return true
        }
    }
    export default {
        INDEX,
        CountNum,
        BLOGVIEW
    }
</script>