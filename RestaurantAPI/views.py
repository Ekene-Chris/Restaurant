from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
import logging

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class MenuItemList(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

class CartList(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        menuitem = get_object_or_404(MenuItem, id=self.request.data['menuitem'])
        serializer.save(user=self.request.user, unit_price=menuitem.price)

class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=self.request.user)
        total = sum(item.price for item in cart_items)
        order = serializer.save(user=self.request.user, total=total)

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
        cart_items.delete()

class ManagerView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({"message": "User added to managers group"}, status.HTTP_200_OK)
        return Response({"message": "Error"}, status.HTTP_400_BAD_REQUEST)

class DeliveryCrewView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.groups.filter(name='Manager').exists():
            username = request.data['username']
            if username:
                user = get_object_or_404(User, username=username)
                delivery_crew = Group.objects.get(name="Delivery crew")
                delivery_crew.user_set.add(user)
                return Response({"message": "User added to delivery crew group"}, status.HTTP_200_OK)
        return Response({"message": "Error"}, status.HTTP_400_BAD_REQUEST)
    
logger = logging.getLogger(__name__)
class AssignOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            if not request.user.groups.filter(name='Manager').exists():
                return Response({'message': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)
            
            order = self.get_object()
            delivery_crew_id = request.data.get('delivery_crew')
            
            if not delivery_crew_id:
                return Response({'message': 'Delivery crew ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                delivery_crew = User.objects.get(pk=delivery_crew_id)
            except User.DoesNotExist:
                return Response({'message': 'Delivery crew user not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if not delivery_crew.groups.filter(name='Delivery crew').exists():
                return Response({'message': 'User is not in delivery crew'}, status=status.HTTP_400_BAD_REQUEST)
            
            order.delivery_crew = delivery_crew
            order.save()
            return Response({'message': 'Order assigned successfully'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error in AssignOrderView: {str(e)}")
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)