import { useDispatch, useSelector } from 'react-redux';
import { bindActionCreators } from '@reduxjs/toolkit';
import * as analyticsActions from '../store/slices/analyticsSlice';
import * as filterActions from '../store/slices/filterSlice';
import * as chatActions from '../store/slices/chatSlice';

export const useActions = () => {
  const dispatch = useDispatch();
  
  return {
    analytics: bindActionCreators(analyticsActions, dispatch),
    filters: bindActionCreators(filterActions, dispatch),
    chat: bindActionCreators(chatActions, dispatch)
  };
};

export const useAppSelector = useSelector; 