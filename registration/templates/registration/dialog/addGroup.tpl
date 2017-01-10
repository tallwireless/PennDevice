<script>

$( "#addGroup button" ).on("click", handleAddGroupForm);

</script>
<div class='addGroupForm'>
<form id='addGroup'>
<div class='fields'>
    <div class="row" id='row-grp'>
        <div class="label">Group Name</div>
        <div class="field"><input name='grp' id='grp' maxlength=32 size=25></div>
        <div id="grp-err" class="hidden"></div>
    <div class="row" id='row-members'>
        <div class="label">Inital Members</div>
        <div class="field"><input name="users" id='users' maxlength=254 size=30></div>
    </div>
    <div class="row" id='row-special'>
        <div class="label">Special VLAN/Role?</div>
        <div class="field"><select name='special'><option selected
        value='false'>No</option><option value='true'>Yes</option></select>
    </div>
</div>
<div class="buttons">
<button id='cancel'>Cancel</button><div class='float-right'><button id='save'>Save</button></div>
</div>
</div>
</div>
