<script>

$( "#addDevice button" ).on("click", handleAddDeviceForm);

</script>
<div class='addDeviceForm'>
<form id='addDevice'>
<div class='fields'>
    <div class="row" id='row-mac'>
        <div class="label">MAC Address</div>
        <div class="field"><input name='mac' id='mac' maxlength=17 size=17></div>
        <div id="mac-err" class="hidden"></div>
    <div class="row" id='row-desc'>
        <div class="label">Description</div>
        <div class="field"><input name="des" id='des' maxlength=254 size=30></div>
    </div>
</div>
<div class="buttons">
<button id='cancel'>Cancel</button><div
class='float-right'><button id='saveadd'> Save &amp; Add</button><button
id='save'>Save</button></div>
</div>
</div>
</div>
