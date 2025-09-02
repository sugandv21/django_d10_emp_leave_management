from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LeaveRequest
from .forms import LeaveRequestForm

def home(request):
    return render(request, "leave/home.html")

#  List View
@login_required
def leave_list(request):
    if request.user.is_superuser or request.user.is_staff:
        leaves = LeaveRequest.objects.all().order_by('-created_at')
    else:
        leaves = LeaveRequest.objects.filter(employee=request.user).order_by('-created_at')
    return render(request, 'leave/leave_list.html', {'leaves': leaves})

#  Create Request
@login_required
def leave_create(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            messages.success(request, "Leave request submitted.")
            return redirect('leave_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave/leave_form.html', {'form': form})

#  Edit (only owner & pending)
@login_required
def leave_edit(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if leave.employee != request.user or leave.status != 'Pending':
        messages.error(request, "You can only edit your own pending requests.")
        return redirect('leave_list')

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave request updated.")
            return redirect('leave_list')
    else:
        form = LeaveRequestForm(instance=leave)
    return render(request, 'leave/leave_form.html', {'form': form})

#  Delete (only owner OR superuser)
@login_required
def leave_delete(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.user == leave.employee or request.user.is_superuser:
        if request.method == 'POST':
            leave.delete()
            messages.success(request, "Leave request deleted.")
            return redirect('leave_list')
        return render(request, 'leave/leave_confirm_delete.html', {'leave': leave})
    messages.error(request, "You do not have permission to delete this request.")
    return redirect('leave_list')

#  Approve (staff & superuser only)
@login_required
def leave_approve(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Only staff/superuser can approve requests.")
        return redirect('leave_list')

    leave = get_object_or_404(LeaveRequest, pk=pk)
    if leave.status == 'Pending':
        leave.status = 'Approved'
        leave.save()
        messages.success(request, "Leave request approved.")
    return redirect('leave_list')

#  Reject (staff & superuser only)
@login_required
def leave_reject(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Only staff/superuser can reject requests.")
        return redirect('leave_list')

    leave = get_object_or_404(LeaveRequest, pk=pk)
    if leave.status == 'Pending':
        leave.status = 'Rejected'
        leave.save()
        messages.success(request, "Leave request rejected.")
    return redirect('leave_list')

# Override Delete (superuser only)
@login_required
def leave_override_delete(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.user.is_superuser:
        if request.method == 'POST':
            leave.delete()
            messages.success(request, "Leave request deleted by superuser.")
            return redirect('leave_list')
        return render(request, 'leave/leave_confirm_delete.html', {'leave': leave})
    messages.error(request, "Only superuser can override and delete requests.")
    return redirect('leave_list')
